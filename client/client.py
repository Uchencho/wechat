import websocket as websocket_client # Importing as websocket client to avoid confusion
import os
from websocket import create_connection

# Remember to run redis server before hitting the endpoints

# Retrieve token from os environment or from postman
token = os.getenv("access_token")

# Initialize websocket
ws_client = websocket_client.WebSocket()

# Connect passing in the token as a query parameter
ws_client.connect(f"ws://localhost:8000/messages?token={token}")
ws = create_connection(f"ws://localhost:8000/messages?token={token}")

# After connecting you can send messages or disconnect at will
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDM3NDc5ODYsImlhdCI6MTYwMzc0MDc4Nn0.Y3cFTWT32qBI7YpiDAm9Fyi7zbbXlyHNErIOdWnUb6A

import websocket, json
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    if message is not None:
        message = json.loads(message)
    print("Am I getting anything at all....")
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send(json.dumps("Hello %d" % i))
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"ws://localhost:8000/messages?token={token}",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
