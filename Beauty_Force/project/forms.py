from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm


class Sign_Up_Form(UserCreationForm):
    inn = forms.CharField(required=True,
                          widget=forms.TextInput(attrs={
                              'class': 'form-control-register',
                              'placeholder': "Введите ИНН компании*",
                              'tabindex': '1',
                              'id': 'name',
                              'name': 'name',
                          }))
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control-register',
                                   'placeholder': "Введите ваше имя*",
                                   'tabindex': '1',
                                   'id': 'name',
                                   'name': 'name',
                               }))
    phoneNumber = forms.CharField(required=True,
                                  widget=forms.TextInput(attrs={
                                      'class': 'form-control-register',
                                      'placeholder': "Введите ваш номер*",
                                      'tabindex': '1',
                                      'id': 'name',
                                      'name': 'name',
                                  }))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control-register',
                                 'placeholder': "Введите вашу почту*",
                                 'tabindex': '1',
                                 'id': 'name',
                                 'name': 'name',
                             }))
    password1 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control-register',
                                    'placeholder': "Придумайте пароль*",
                                    'tabindex': '1',
                                    'id': 'name',
                                    'name': 'name',
                                }))
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control-register',
                                    'placeholder': "Повторите новый пароль*",
                                    'tabindex': '1',
                                    'id': 'name',
                                    'name': 'name',
                                }))

    class Meta:
        model = Users
        fields = [
            'inn',
            'username',
            'phoneNumber',
            'email',
            'password1',
            'password2',
        ]


class Login_Form(AuthenticationForm):
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control-login',
                                   'placeholder': "Введите вашу почту",
                                   'tabindex': '1',
                                   'id': 'name',
                                   'name': 'name',
                               }))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control-login',
                                   'placeholder': "Введите пароль",
                                   'tabindex': '1',
                                   'id': 'name',
                                   'name': 'name',
                               }))

    class Meta:
        model = Users
        fields = [
            'username',
            'password',
        ]


class Change_Password_Form(PasswordChangeForm):
    old_password = forms.CharField(required=True,
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control-login',
                                       'placeholder': "Введите старый пароль",
                                       'tabindex': '1',
                                       'id': 'name',
                                       'name': 'name',
                                   }))
    new_password1 = forms.CharField(required=True,
                                    widget=forms.PasswordInput(attrs={
                                        'class': 'form-control-login',
                                        'placeholder': "Введите новый пароль",
                                        'tabindex': '1',
                                        'id': 'name',
                                        'name': 'name',
                                    }))
    new_password2 = forms.CharField(required=True,
                                    widget=forms.PasswordInput(attrs={
                                        'class': 'form-control-login',
                                        'placeholder': "Повторите новый пароль",
                                        'tabindex': '1',
                                        'id': 'name',
                                        'name': 'name',
                                    }))

    class Meta:
        model = Users
        fields = [
            'old_password',
            'new_password1',
            'new_password2',
        ]
