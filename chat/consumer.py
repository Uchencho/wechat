from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer

from .models import Thread, ChatMessage

class ChatConsumer(SyncConsumer):
    """
    Gives the user the ability to chat
    """
    def websocket_connect(self, event):
        print("Connected", event)
        self.send({
            "type" : "websocket.accept"
        })
        print("\n\nChannel Name is", self.channel_name, "\n\n")
        
        user = self.scope['user']
        user.online = True
        user.save()

        self.send({
            "type" : "websocket.send",
            "text" : "Connected"
        })
        

    def websocket_receive(self, event):
        # when a message is received from the websocket

        #Send the message using redis to the other end
        # How does it know which specific chat to listen to?
        self.send({
            "type" : "websocket.send",
            "text" : "attached " + event["text"]
        })
    
        # Archive the message in the DB
        user = self.scope['user']
        other_username = event["text"]["user_id"]
        if not other_username:
            # Handle it
            print("HI")

        thread_obj, _ = Thread.objects.get_or_new(user, other_username)
        if not thread_obj:
           # Handle it 
           print("Hello")
        
        ChatMessage.objects.create(thread=thread_obj, user=user, message=event["text"])
        print("receive", event)

    def websocket_disconnect(self, event):
        # when the socket disconnects
        print("disconnected", event)
        user = self.scope['user']
        user.online = False
        user.save()
        raise StopConsumer("Consumer disconnected")

