from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .forms import UserProfileForm
from .serializers import UserSerializer


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('auth')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        return render(request, 'register.html')


class UserAuthAndLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'auth.html')

    def get(self, request):
        return render(request, 'auth.html')


def google(request):
    return render(request, 'google.html')

def profile(request):
    return render(request, 'profile.html')


# передача данных в профиль html
@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


# изменение профиля
@login_required
def edit_profile(request):
    user_profile = get_object_or_404(User, username=request.user)  #  username=request.user - возвращает только текущего пользователя
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})

