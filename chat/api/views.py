from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

from accounts.models import User
from chat.models import Thread
from .serializers import UserSerializer

class UserView(generics.ListAPIView):
    serializer_class        = UserSerializer
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [SessionAuthentication]

    def get_queryset(self):
        return User.objects.filter(email__iexact=self.request.user.email)


def string_to_bool(the_string):
    if the_string == "true":
        return True
    elif the_string == "false":
        return False
    else:
        return ""


class ChatHistory(APIView):

    """
    Retrieve the list of users a specific user has had a conversation with
    """

    def get(self, request):
        qs = Thread.objects.by_user(request.user)
        if not qs.exists():
            return Response({"message" : "success", "data" : {}})

        chat_det = [{"id" : chatter.id, "username" : chatter.first.username if not request.user.username else chatter.second.username} for chatter in qs]
        return Response({"message" : "success", "data" : chat_det})


class AllUsers(APIView):

    """
    Retrieve a list of users with the option of filtering only online users
    """

    def get(self, request):
        online  = request.GET.get('online', None)

        if not online:
            qs = User.objects.filter(is_staff=False)
        else:
            online = string_to_bool(online)
            if type(online) != bool:
                return Response({"error" : "Online query parameter must be either 'true' or 'false'"}, status=status.HTTP_400_BAD_REQUEST)
            qs = User.objects.filter(is_staff=False, online=online)

        if not qs.exists():
            return Response({"message" : "success", "data" : {}})

        user_l = [{"id" : the_user.id, "username" : the_user.username, "online" : the_user.online} for the_user in qs if the_user != request.user]
        return Response({"message" : "success", "data" : user_l})
    