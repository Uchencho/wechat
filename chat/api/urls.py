from django.contrib import admin
from django.urls import path, re_path

from .views import ChatHistory, AllUsers

urlpatterns = [
    path('history', ChatHistory.as_view(), name='chat-history'),
    path('', AllUsers.as_view(), name='all-users'),
]