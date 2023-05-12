from django.urls import path, re_path
from . import views
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/fashion_news/$', consumers.FashionNewsConsumer.as_asgi()),
]

urlpatterns = [
    path('fashion_news/', views.fashion_news, name='fashion_news'),
]
