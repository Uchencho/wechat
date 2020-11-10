from rest_framework.views import APIView
from rest_framework import exceptions, status, generics
from rest_framework.response import Response
from django.conf import settings
import jwt, json
from datetime import timedelta
from django.utils import timezone

from accounts.models import User
from .serializers import UserSerializer, UserRegisterSerializer, UpdateProfileSerializer
from .permissions import BasicToken
from .utils import generate_access_token, generate_refresh_token


class Login(APIView):
    permission_classes      = [BasicToken]
    authentication_classes  = []

    def get_serializer_context(self, *args, **kwargs):
        return {"request" : self.request}

    def post(self, request):
        email = request.data.get('email', "Not Sent")
        password = request.data.get('password', "Not Sent")
        response = Response()

        if email == "Not Sent" or password == "Not Sent":
            raise exceptions.AuthenticationFailed("Invalid payload")

        user = User.objects.filter(email__iexact=email).first()
        if user == None or not user.check_password(password):
            raise exceptions.AuthenticationFailed("Email or password is incorrect")

        user = User.objects.filter(email__iexact=email).first()
        user.last_login = timezone.now()
        user.save()

        serialized_user = UserSerializer(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        serialized_user['access_token'] = access_token
        response.data = {"message" : "success", "data" : serialized_user}
        return response


class RefreshToken(APIView):
    permission_classes      = []
    authentication_classes  = []

    def post(self, request):
        refresh_token = request.COOKIES.get('refreshtoken', "None")
        if refresh_token == "None":
            raise exceptions.AuthenticationFailed("Authentication Credentials were not provided")

        try:
            payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET,
                                    algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Expired Refresh Token, please login again")
        except:
            raise exceptions.AuthenticationFailed("Can't decode, please login again")

        user = User.objects.filter(id=payload.get("user_id")).first()
        if user == None or not user.is_active:
            raise exceptions.AuthenticationFailed("User not found")

        new_access_token = generate_access_token(user)
        return Response({"message" : "success",
         "data":{"access_token": new_access_token}}, status=status.HTTP_201_CREATED)


class RegisterAPIView(APIView):
    permission_classes      = [BasicToken]
    authentication_classes  = []

    def post(self, request):
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid():

            user = serializer.save()
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            user.last_login = timezone.now()
            user.save()

            serialized_user = serializer.data
            serialized_user['access_token'] = access_token
            data = {"message" : "success", "data" : serialized_user}
            
            response = Response()
            response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
            response.data = data
            return response

        else:
            data = serializer.errors
            response = Response()
            response.delete_cookie(key='refreshtoken')
            response.status_code = status.HTTP_400_BAD_REQUEST
            if len(data) > 1:
                response.data = {"error":"invalid payload"}
                return response
            response.data = {"error":list(data.values())[0][0]}
            return response


class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("refreshtoken")
        response.data = {"message" : "logged out successfully", "data" : {}}
        response.status_code = status.HTTP_204_NO_CONTENT
        return response


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    queryset                = User.objects.all()
    serializer_class        = UpdateProfileSerializer

    def get_object(self):
        """
        This handles the issue of pk in the url
        """
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request):
        user = request.user
        user_data = UpdateProfileSerializer(user).data
        return Response({"message" : "success", "data" : user_data})
        # return User.objects.filter(username__iexact=self.request.user.username)

    def put(self, request, *args, **kwargs):
        updated = self.update(request, *args, **kwargs)
        return Response({"message" : "success", "data" : updated.data})

    def patch(self, request, *args, **kwargs):
        patched = self.partial_update(request, *args, **kwargs)
        return Response({"message" : "success", "data" : patched.data})

