import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from fashionShows.consumers import FashionNewsConsumer
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<имя_вашего_проекта>.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/news/$', FashionNewsConsumer.as_asgi()),
        ])
    ),
})

# Используем Redis в качестве канального слоя
channel_layer = get_channel_layer()


