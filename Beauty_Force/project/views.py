from django.shortcuts import render, get_object_or_404

from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import CreateView

from django.urls import reverse_lazy

from django.core.mail import send_mail

from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template.loader import render_to_string

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .forms import *
from .models import *
from .token import *


class Main_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class Brands_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'brands.html')


class Catalog_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'catalog.html')


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


class Register_Page(SuccessMessageMixin, CreateView):
    form_class = Sign_Up_Form
    success_url = reverse_lazy('main_page')
    template_name = 'register.html'
    success_message = 'Вам на почту отправлено письмо для активации аккаунта'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
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
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class Login_Page(SuccessMessageMixin, LoginView):
    form_class = Login_Form
    success_url = reverse_lazy('personal_account')
    template_name = 'login.html'
    success_message = 'Вы успешно вошли в систему'

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


class Users_Lk_Page(View):
    success_message = 'Вам на почту отправлена ссылка на изменение пароля'
    error_message = 'Что-то пошло не так, письмо не было отправлено'

    success_message_add_adresses = "Адрес доставки успешно добавлен"
    error_message_add_adresses = "Что-то пошло не так, пожалуйста, попробуйте снова"

    HARUHARU_WONDER = Product.objects.filter(brand=2)
    DR_GLODERM = Product.objects.filter(brand=1)

    def get(self, request, *args, **kwargs):
        current_user = Users.objects.get(username=request.user)
        total_amount = current_user.total_amount_of_orders
        total_amount_all_percent = 0
        sale = current_user.discount_percentage + 1

        if current_user.discount_percentage == 5:
            sale = 5

        if total_amount < 50000:
            total_amount_all_percent = 50000 - total_amount
        elif 50000 <= total_amount < 100000:
            total_amount_all_percent = 100000 - total_amount
        elif 100000 <= total_amount < 150000:
            total_amount_all_percent = 150000 - total_amount
        elif 150000 <= total_amount < 200000:
            total_amount_all_percent = 200000 - total_amount
        elif 200000 <= total_amount < 250000:
            total_amount_all_percent = 250000 - total_amount
        elif total_amount >= 250000:
            total_amount_all_percent = total_amount

        context = {
            'sale': sale,
            'total_amount_all_percent': total_amount_all_percent,
            'HARUHARU_WONDER': self.HARUHARU_WONDER,
            'DR_GLODERM': self.DR_GLODERM,
        }
        return render(
            request,
            'users_lk.html',
            context=context
        )

    def post(self, request, *args, **kwargs):
        user = Users.objects.get(username=request.user)
        current_user = Users.objects.get(username=request.user)
        total_amount = current_user.total_amount_of_orders
        total_amount_all_percent = 0
        sale = current_user.discount_percentage + 1

        if current_user.discount_percentage == 5:
            sale = 5

        if total_amount < 50000:
            total_amount_all_percent = 50000 - total_amount
        elif 50000 <= total_amount < 100000:
            total_amount_all_percent = 100000 - total_amount
        elif 100000 <= total_amount < 150000:
            total_amount_all_percent = 150000 - total_amount
        elif 150000 <= total_amount < 200000:
            total_amount_all_percent = 200000 - total_amount
        elif 200000 <= total_amount < 250000:
            total_amount_all_percent = 250000 - total_amount
        elif total_amount >= 250000:
            total_amount_all_percent = total_amount

        context = {
            'sale': sale,
            'total_amount_all_percent': total_amount_all_percent,
        }

        if request.POST.get('acсount-email'):
            mail = request.POST.get('acсount-email')
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': '127.0.0.1:8000',
            })
            try:
                messages.success(request, self.success_message)
                send_mail(
                    'Изменение пароля на сайте Beauty Force',
                    message,
                    'reg@beforce.ru',
                    [mail],
                    fail_silently=False,
                )
            except:
                messages.error(request, self.error_message)

        elif request.POST.get('city'):
            city = request.POST.get('city')
            street = request.POST.get('street')
            home = request.POST.get('home')
            entrance = request.POST.get('entrance')
            floor = request.POST.get('floor')
            apartment_or_office = request.POST.get('apartment_or_office')
            try:
                Delivery_Addresses.objects.create(
                    recipient=user,
                    city=city,
                    street=street,
                    home=home,
                    entrance=entrance,
                    floor=floor,
                    apartment_or_office=apartment_or_office
                )
                messages.success(request, self.success_message_add_adresses)
            except:
                messages.error(request, self.error_message_add_adresses)

        return render(
            request,
            'users_lk.html',
            context=context
        )


class Catalog_Item(View):

    def get(self, request, title, slug, *args, **kwargs):

        product = get_object_or_404(Product, title=title, slug=slug)
        context = {
            'product': product,
        }
        return render(request, 'catalog_item.html', context=context)


class Password_Reset(View):

    def get(self, request, *args, **kwargs):

        form = Change_Password_Form(request.user)
        context = {
            'form': form
        }
        return render(request, 'change_password.html', context=context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = Change_Password_Form(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Ваш пароль успешно изменен')
                return HttpResponseRedirect('/personal_account/')
            else:
                messages.error(request, 'Пароль не был изменен.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form
        })


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
        messages.success(request, 'Вы успешно прошли верификацию.')
        return HttpResponseRedirect('/')
    else:
        messages.error(request, 'Верификация не пройдена.')
        return HttpResponseRedirect('/')
