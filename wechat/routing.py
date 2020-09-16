from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from chat.consumer import ChatConsumer

application = ProtocolTypeRouter({
    # Empty for now, (http-django views is added by default)
    'websocket' : AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^messages/(?<id>[\w.@+-]+)/$", ChatConsumer),
                ]
            )
        )
    )
})

# ws://ourdomain/messages/<username>
# wss://ourdomeain/messages/<username> for production