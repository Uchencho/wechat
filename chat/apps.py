from django.apps import AppConfig


class ChatConfig(AppConfig):
    name = 'chat'


# import websockets, asyncio
# def test_url(url, data=""):
#      async def inner():
#          async with websockets.connect(url) as websocket:
#              await websocket.send(data)
#      return asyncio.get_event_loop().run_until_complete(inner())