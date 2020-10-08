import jwt
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from rest_framework.response import Response
from django.conf import settings

from accounts.models import User


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        authorization_header = request.headers.get("Authorization")

        if not authorization_header:
            return None

        try:
            access_token = get_authorization_header(request).decode('utf-8').split(" ")[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Access token expired")
        except IndexError:
            raise exceptions.AuthenticationFailed("Access token not sent")
        except:
            raise exceptions.AuthenticationFailed("Authentication failed")

        user = User.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is inactive")

        return (user, None)

