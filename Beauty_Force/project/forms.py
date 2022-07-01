from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(0, 100)]


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


class Add_To_Cart_Form(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, widget=forms.Select(
        attrs={
            'class': 'quantity'
        }
    ))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    class Meta:
        fields = [
            'quantity',
            'update',
        ]


class Contact_Form(forms.Form):
    telephone_number = forms.CharField(required=True,
                                       widget=forms.TextInput(attrs={
                                           'class': 'form-control',
                                           'placeholder': "Телефон",
                                           'tabindex': '1',
                                           'id': 'telephone',
                                           'name': 'telephone',
                                       }))
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': "Контактное лицо",
                               'tabindex': '2',
                               'id': 'name',
                               'name': 'name',
                           }))

    class Meta:
        fields = [
            'telephone_number',
            'name',
        ]


class Get_Price_Form(forms.Form):
    telephone_number = forms.CharField(required=True,
                                       widget=forms.TextInput(attrs={
                                           'class': 'form-control',
                                           'placeholder': "Телефон",
                                           'tabindex': '1',
                                           'id': 'telephone_number',
                                           'name': 'telephone_number',
                                       }))
    email = forms.CharField(required=True,
                            widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder': "Почта",
                                'tabindex': '1',
                                'id': 'email',
                                'name': 'email',
                            }))
    contact_name = forms.CharField(required=True,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': "Контактное лицо",
                                       'tabindex': '1',
                                       'id': 'contact_name',
                                       'name': 'contact_name',
                                   }))
    company_name = forms.CharField(required=True,
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': "Компания",
                                       'tabindex': '1',
                                       'id': 'company_name',
                                       'name': 'company_name',
                                   }))

    class Meta:
        fields = [
            'telephone_number',
            'email',
            'contact_name',
            'company_name',
        ]


class Send_Mail_Admin_Form(forms.Form):
    subject = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': "Введите тему письма",
                                  'tabindex': '1',
                                  'id': 'subject',
                                  'name': 'subject',
                              }))
    message = forms.CharField(required=True,
                              widget=forms.Textarea(attrs={
                                  'class': 'form-control',
                                  'placeholder': "Введите сообщение",
                                  'tabindex': '1',
                                  'id': 'message',
                                  'name': 'message',
                              }))

    class Meta:
        fields = [
            'subject',
            'message',
        ]
