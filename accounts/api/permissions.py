from rest_framework.authentication import get_authorization_header
from rest_framework import permissions, status
from rest_framework.views import exception_handler

from dotenv import load_dotenv
import os
load_dotenv('/home/uchencho/Documents/Notebooks/Django Apps/wechat-p/wechat')

class BasicToken(permissions.BasePermission):
    message = "No token was passed"

    def has_permission(self, request, view):
        token = os.getenv("token", None)
        if not token:
            raise EnvironmentError("Environment variable not found")
        try:
            in_token = get_authorization_header(request).decode('utf-8').split(" ")[1]
        except IndexError:
            return False
        if token != in_token:
            return False
        return True


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 403 or response.status_code == 401:
            response.delete_cookie("refreshtoken")
            response.status_code = status.HTTP_401_UNAUTHORIZED
        try:
            incoming_error = response.data["detail"]
            response.data = {"error" : incoming_error}
        except:
            pass
    return response

