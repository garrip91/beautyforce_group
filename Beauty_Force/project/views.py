from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.core.mail import send_mail

from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .forms import *
from .models import *
from .token import *
from django.contrib.auth import get_user_model


class Main_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class Brands_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'brands.html')


class Catalog_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'catalog.html')


class Catalog_Item(View):
    # def get(self, request, name, *args, **kwargs):
    def get(self, request, *args, **kwargs):
        return render(request, 'catalog_item.html')


class Brand_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'brand_page.html')


class Partnership_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'partnership.html')


class Press_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'press.html')


class Contacts_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contacts.html')


class Privacy_Policy_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'privacy.html')


class Register_Page(CreateView):
    form_class = Sign_Up_Form
    success_url = reverse_lazy('main_page')
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        username = form.cleaned_data['username']
        mail = form.cleaned_data['email']
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(
            'Подтверждение регистрации на сайте Beauty Force',
            message,
            'reg@beforce.ru',
            [mail],
            fail_silently=False,
        )
        return HttpResponse('Please confirm your email address to complete the registration')

    def form_invalid(self, form):
        print(form)
        return super().form_invalid(form)


class Login_Page(LoginView):
    form_class = Login_Form
    success_url = reverse_lazy('main_page')
    template_name = 'login.html'

    def form_valid(self, form):
        return super(Login_Page, self).form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class B2B_Catalog_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'b2b_catalog.html')


class Basket_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'basket.html')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
