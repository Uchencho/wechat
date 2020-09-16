import asyncio, json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Connected", event)
        await self.send({
            "type" : "websocket.accept"
        })
        other_user = self.scope['url_route']['kwargs']['username']
        me         = self.scope['user']
        print(other_user, me)

    async def websocket_receive(self, event):
        # when a message is received from the websocket
        print("receive", event)

    async def websocket_disconnect(self, event):
        # when the socket disconnects
        print("disconnected", event)  

