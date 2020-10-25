import websocket as websocket_client # Importing as websocket client to avoid confusion
import os

# Remember to run redis server before hitting the endpoints

# Retrieve token from os environment or from postman
token = os.getenv("access_token")

# Initialize websocket
ws_client = websocket_client.WebSocket()

# Connect passing in the token as a query parameter
ws_client.connect(f"ws://localhost:8000/messages?token={token}")

# After connecting you can send messages or disconnect at will