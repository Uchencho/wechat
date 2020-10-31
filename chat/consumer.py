from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

from .models import Thread, ChatMessage

class ChatConsumer(SyncConsumer):
    """
    Gives the user the ability to chat
    """
    def websocket_connect(self, event):

        print("Event is ",  event)
        try:
            other_username = event["text"]["receiver_username"]
            receiver_id = event["text"]["receiver_id"]
            print("\nOther username is ", other_username, "and receiver id is ", receiver_id, "\n")
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
            "type" : "websocket.send",
            "text" : "Connected"
        })
        

    def websocket_receive(self, event):

        message = event['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'websocket.send',
                'message' : message
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


def room_formatter(x):
    if len(x) != 2:
        raise IndexError("X should be contain two integers")
    x = sorted(x)
    return f"room_{x[0]}_{x[1]}"
