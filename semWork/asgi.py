import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.layers import get_channel_layer
from fashionShows import urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semWork.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(urls.websocket_urlpatterns)
    ),
})

channel_layer = get_channel_layer()