from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from accounts.models import User
from .serializers import UserSerializer

class UserView(generics.ListAPIView):
    serializer_class        = UserSerializer
    permission_classes      = [IsAuthenticated]
    authentication_classes  = [SessionAuthentication]

    def get_queryset(self):
        return User.objects.filter(email__iexact=self.request.user.email)

