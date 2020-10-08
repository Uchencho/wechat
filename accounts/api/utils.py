from datetime import datetime, timedelta
import jwt
from django.conf import settings
from rest_framework.views import exception_handler

def generate_access_token(user):

    access_token_payload = {
        'user_id' : user.id,
        'exp': datetime.utcnow() + timedelta(hours=2),
        'iat' : datetime.utcnow(),
    }

    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY,
                            algorithm='HS256').decode('utf-8')
    return access_token


def generate_refresh_token(user):

    refresh_token_payload = {
        'user_id' : user.id,
        'exp': datetime.utcnow() + timedelta(hours=6),
        'iat' : datetime.utcnow(),
    }

    refresh_token = jwt.encode(refresh_token_payload, settings.REFRESH_TOKEN_SECRET,
                            algorithm='HS256').decode('utf-8')
    return refresh_token


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now delete the cookies that would have otherwise being sent.
    if response is not None:
        response.delete_cookie("refreshtoken")
    return response
