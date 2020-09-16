from rest_framework.authentication import get_authorization_header
from rest_framework import permissions

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

