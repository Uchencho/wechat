from django.conf.urls import url
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from chat.consumer import ChatConsumer
from chat.channelMiddleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    # Empty for now, (http-django views is added by default)
    # 'websocket' : AllowedHostsOriginValidator(
    #         TokenAuthMiddleware(
    #             URLRouter(
    #                 [
    #                     url("messages", ChatConsumer),
    #                 ]
    #             )
    #         )
    #     )
    'websocket' : URLRouter(
                    [
                        url("messages", ChatConsumer),
                    ]
                )
            
    # 'websocket' : AllowedHostsOriginValidator(
    #     AuthMiddlewareStack(
    #         URLRouter(
    #             [
    #                 url(r"^messages/(?<username>[\w.@+-]+)/$", ChatConsumer),
    #             ]
    #         )
    #     )
    # )
})

# ws://ourdomain/messages/<username>
# wss://ourdomeain/messages/<username> for production