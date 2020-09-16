
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.api.urls', namespace='api-accounts')),
    path('messages/', include('chat.api.urls')),

]


# https://github.com/codingforentrepreneurs/Rapid-ChatXChannels