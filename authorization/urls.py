from django.urls import path, include
from . import views
from .views import UserRegistrationAPIView, UserAuthAndLoginAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('auth/', UserAuthAndLoginAPIView.as_view(), name='auth'),
    path('google/', views.google, name='google')
]
