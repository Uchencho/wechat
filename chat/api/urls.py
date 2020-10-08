from django.contrib import admin
from django.urls import path, re_path

from .views import UserView

urlpatterns = [
    re_path(r"^(?P<username>[\w.@+-]+)", UserView.as_view()),
]