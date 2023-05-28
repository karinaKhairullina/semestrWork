from django.urls import path
from . import views


urlpatterns = [
    path('subscription/', views.subscription, name='subscription'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('subscribe/<int:user_id>/', views.subscribe, name='subscribe'),
]