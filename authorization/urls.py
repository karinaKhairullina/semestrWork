from django.urls import path
from .views import UserRegistrationAPIView, UserAuthAndLoginAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('auth/', UserAuthAndLoginAPIView.as_view(), name='auth'),
]
