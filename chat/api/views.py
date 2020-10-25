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


class ChatHistory(APIView):

    def get(self, request):
        qs = Thread.objects.by_user(request.user)
        if not qs.exists():
            return Response({"message" : "success", "data" : {}})

        chat_det = [{"id" : chatter.id, "username" : chatter.username} for chatter in qs]
        return Response({"message" : "success", "data" : chat_det})
