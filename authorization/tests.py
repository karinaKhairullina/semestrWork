from .forms import UserProfileForm
from .forms import ResetPasswordForm
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


class UserProfileFormTest(TestCase):
    def test_form_fields(self):
        form = UserProfileForm()
        self.assertTrue('username' in form.fields)
        self.assertTrue('email' in form.fields)
        self.assertTrue('first_name' in form.fields)
        self.assertTrue('last_name' in form.fields)

    def test_form_labels(self):
        form = UserProfileForm()
        self.assertEqual(form.fields['username'].label, 'Логин')
        self.assertEqual(form.fields['email'].label, 'Email')
        self.assertEqual(form.fields['first_name'].label, 'Имя')
        self.assertEqual(form.fields['last_name'].label, 'Фамилия')

class ResetPasswordFormTest(TestCase):

    def test_password_match_success(self):
        form_data = {'new_password': 'password1', 'confirm_password': 'password1'}
        form = ResetPasswordForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserModelTest(TestCase):
    def test_create_user(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        user = User.objects.get(username='admin')
        self.assertEqual(user.email, 'admin@example.com')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

User = get_user_model()

class UserSerializerTest(TestCase):
    def test_create_user(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('testpass'))

