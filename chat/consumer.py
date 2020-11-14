from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from urllib.parse import parse_qs
import json

from .models import Thread, ChatMessage
from chat.api.serializers import ChatMessageSerializer

class ChatConsumer(SyncConsumer):
    """
    Gives the user the ability to chat
    """
    def websocket_connect(self, event):

        try:
            queryParams = parse_qs(self.scope["query_string"].decode("utf8"))
            other_username = queryParams["receiver_username"][0]
            receiver_id = queryParams["receiver_id"][0]
        except KeyError:
            raise StopConsumer("Invalid Payload")

        user = self.scope['user']

        thread_obj, _ = Thread.objects.get_or_new(user, other_username)
        if not thread_obj:
           raise StopConsumer("Invalid Payload")

        self.thread_obj = thread_obj
        self.room_group_name = room_formatter([int(user.id), int(receiver_id)])

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        user = self.scope['user']
        user.online = True
        user.save()

        self.send({
            "type" : "websocket.accept",
            "text" : "serialized_data"
        })  

    def websocket_receive(self, event):

        msg_json = json.loads(event['text'])
        message = msg_json['message']
        resp = {"message" : message}
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : json.dumps(resp)
            }
        )
        user = self.scope['user']
        ChatMessage.objects.create(thread=self.thread_obj, user=user, message=message)

    def websocket_disconnect(self, event):

        user = self.scope['user']
        user.online = False
        user.save()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        raise StopConsumer("Consumer disconnected")

    def chat_message(self, event):
        incoming_message = event.get('message', None)
        if incoming_message:
            message = json.loads(incoming_message)
        else:
            message = "received nada"
        resp = {"message" : message}
        self.send({
            'type' : "websocket.send",
            'text' : json.dumps(resp)
        })


def room_formatter(x):
    if len(x) != 2:
        raise IndexError("X should contain only two integers")
    x = sorted(x)
    return f"room_{x[0]}_{x[1]}"
