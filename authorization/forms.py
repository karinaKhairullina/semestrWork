from django import forms
from .models import User


class UserProfileForm(forms.ModelForm):
    """
    Форма профиля пользователя.

    Поля:
    - username (строка): логин пользователя
    - email (строка): email пользователя
    - first_name (строка): имя пользователя
    - last_name (строка): фамилия пользователя
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Логин',
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }


class EmailForm(forms.Form):
    email = forms.EmailField()


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

