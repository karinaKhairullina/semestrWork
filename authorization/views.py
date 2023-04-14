from django.shortcuts import render, redirect
from django.contrib import messages
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required


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


# только для зарегистрированных пользователей
@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


