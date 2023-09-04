# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.urls import path
from .consumers import *

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        [
            path("ws/some_path/", ProgressConsumer.as_asgi()),
            # Add more WebSocket routing patterns as needed
        ]
    ),
})