import asyncio, json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

from .models import Thread, ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Connected", event)
        await self.send({
            "type" : "websocket.accept"
        })

        # other_user = self.scope['url_route']['kwargs']['username']
        # user = self.scope['user']
        print("\n\n", "user", "\n\n")

        await self.send({
            "type" : "websocket.send",
            "text" : "Can you see me"
        })
        

    async def websocket_receive(self, event):
        # when a message is received from the websocket
        print("receive", event)

    async def websocket_disconnect(self, event):
        # when the socket disconnects
        print("disconnected", event)  


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         print("It connected")
#         self.accept()

#     def disconnect(self):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         self.send(text_data=json.dumps({
#             'message' : message
#         }))
