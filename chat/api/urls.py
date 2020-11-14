from django.contrib import admin
from django.urls import path, re_path

from .views import ChatHistory, AllUsers, MessageHistory

urlpatterns = [
    path('history', ChatHistory.as_view(), name='chat-history'),
    path('history/messages', MessageHistory.as_view(), name='message-history'),
    path('', AllUsers.as_view(), name='all-users'),
]