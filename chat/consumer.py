from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer


class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Connected", event)
        self.send({
            "type" : "websocket.accept"
        })

        # other_user = self.scope['url_route']['kwargs']['username']
        user = self.scope['user']
        print("\n\n", user, "\n\n")

        self.send({
            "type" : "websocket.send",
            "text" : "Can you see me"
        })
        

    def websocket_receive(self, event):
        # when a message is received from the websocket
        print("receive", event)

    def websocket_disconnect(self, event):
        # when the socket disconnects
        print("disconnected", event)
        raise StopConsumer("Consumer disconnected")

