from . import views
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/fashion_news/', consumers.FashionNewsConsumer.as_asgi()),
]
urlpatterns = [
    path('fashion_news/', views.fashion_news, name='fashion_news'),
]
