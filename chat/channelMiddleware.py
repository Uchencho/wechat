from django.db import close_old_connections
from channels.db import database_sync_to_async
from rest_framework import exceptions
from urllib.parse import parse_qs
import jwt
from django.conf import settings

from accounts.models import User

@database_sync_to_async
def get_user(user_id):
    user = User.objects.filter(id=user_id).first()
    if user is None or not user.is_active:
        return None
    return user

class TokenAuthMiddlewareInstance:
    """
    Custom token auth middleware
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        close_old_connections()
        try:
            token = parse_qs(self.scope["query_string"].decode("utf8"))["token"][0]
        except KeyError:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return None
        except IndexError:
            return None
        except:
            return None

        user = await get_user(payload['user_id'])
        if not user:
            return None

        self.scope['user'] = user
        inner = self.inner(self.scope)

        return await inner(receive, send)


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)

