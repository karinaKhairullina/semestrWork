from django.urls import path
from . import views
from .views import UserRegistrationAPIView, UserAuthAndLoginAPIView, send_email_view,reset_password_view

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('auth/', UserAuthAndLoginAPIView.as_view(), name='auth'),
    path('google/', views.google, name='google'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('send-email/', send_email_view, name='send_email'),
    path('reset-password/<int:user_id>/', reset_password_view, name='reset_password'),
]
