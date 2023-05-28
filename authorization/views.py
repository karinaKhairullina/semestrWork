from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .forms import UserProfileForm, ResetPasswordForm
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from authorization.tasks import send_email_task
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class UserRegistrationAPIView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        """
        Регистрирует нового пользователя.

        Args:
            request (HttpRequest): HTTP-запрос.

        Returns:
            HttpResponse или Redirect: Возвращает HTTP-ответ или перенаправление.

        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('auth')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Отображает страницу регистрации.

        Args:
            request (HttpRequest): HTTP-запрос.

        Returns:
            HttpResponse: Возвращает HTTP-ответ.

        """
        return render(request, 'register.html')


class UserAuthAndLoginAPIView(APIView):
    def post(self, request):
        """
        Аутентификация пользователя и вход в систему.

        Args:
            request (HttpRequest): HTTP-запрос.

        Returns:
            HttpResponse или Redirect: Возвращает HTTP-ответ или перенаправление.

        """
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password, email=email)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'auth.html')

    def get(self, request):
        """
        Отображает страницу аутентификации.

        Args:
            request (HttpRequest): HTTP-запрос.

        Returns:
            HttpResponse: Возвращает HTTP-ответ.

        """
        return render(request, 'auth.html')


def google(request):
    """
    Отображает страницу Google.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        HttpResponse: Возвращает HTTP-ответ.

    """
    return render(request, 'google.html')


@login_required
def profile(request):
    """
    Отображает страницу профиля пользователя.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        HttpResponse: Возвращает HTTP-ответ.

    """
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def edit_profile(request):
    """
    Изменяет профиль пользователя.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        HttpResponse или Redirect: Возвращает HTTP-ответ или перенаправление.

    """
    user_profile = get_object_or_404(User, username=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})


def logout_view(request):
    """
    Выход пользователя из системы.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        Redirect: Возвращает перенаправление.

    """
    logout(request)
    return redirect('auth')



def send_email_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponseBadRequest('Некорректный email!')

        User = get_user_model()
        user = User.objects.get(email=email)
        send_email_task.delay(user.id)
        return render(request, 'front.html', {'message': 'Отправлено успешно!', 'flag': True})
    else:
        return render(request, 'front.html', {'flag': False})


def reset_password_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            user = authenticate(request, username=user.username, password=new_password)
            if user is not None:
                login(request, user)
                return redirect('auth')
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form, 'user': user})






