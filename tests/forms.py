from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

from tests.models import *


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )


class RegisterForm(UserCreationForm):
    username = UsernameField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
    )


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('answer',)
