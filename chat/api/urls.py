from django.contrib import admin
from django.urls import path, re_path

from .views import ChatHistory

urlpatterns = [
    path('history', ChatHistory.as_view(), name='chat-history'),
]