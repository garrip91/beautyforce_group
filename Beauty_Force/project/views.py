from itertools import product
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

from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .forms import *
from .models import *
from .token import *
from .mixins import *

import simplejson
from decimal import Decimal


class Main_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class Brands_Page(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'brands.html')


class Catalog_Page(View):

    all_products = Product.objects.all()
    brands = Brands.objects.all()

    def get(self, request, *args, **kwargs):

        context = {
            'all_products': self.all_products,
            'brands': self.brands,
            'get_price': Get_Price_Form(),
        }

        return render(request, 'catalog.html', context=context)

    def post(self, request, *args, **kwargs):
        
        form = Get_Price_Form(request.POST)

        context = {
            'get_price': Get_Price_Form(),
            'all_products': self.all_products,
            'brands': self.brands,
        }
       
        if form.is_valid():
            telephone_number = form.cleaned_data['telephone_number']
            email = form.cleaned_data['email']
            contact_name = form.cleaned_data['contact_name']
            company_name = form.cleaned_data['company_name']
            try:
                send_mail(
                    'Прайс Beauty Force',
                    'Добрый день {}! \n Запрошенный прайс во вложении.'.format(
                        contact_name,
                    ),
                    'reg@beforce.ru',
                    [email],
                    fail_silently=False,
                )
                
                send_mail(
                    'Заказ выгрузки прайса',
                    'Контактное лицо {}, телефон {}, компания {}'.format(
                        contact_name,
                        telephone_number,
                        company_name
                    ),
                    'reg@beforce.ru',
                    ['reg@beforce.ru'],
                    fail_silently=False,
                )
                messages.success(request, "price")
            except:
                messages.error(request, "Что-то пошло не так, попробуйте снова.")
        return render(request, 'catalog.html', context=context)

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


class Users_Lk_Page(View):
    success_message = 'Вам на почту отправлена ссылка на изменение пароля'
    error_message = 'Что-то пошло не так, письмо не было отправлено'

    success_message_add_adresses = "Адрес доставки успешно добавлен"
    error_message_add_adresses = "Что-то пошло не так, пожалуйста, попробуйте снова"

    all_products = Product.objects.all()
    add_to_cart = Add_To_Cart_Form
    brands = Brands.objects.all()
    contact_form = Contact_Form
    bestsellers_line = Bestsellers_Line.objects.all()[1:]
    

    def get(self, request, *args, **kwargs):
        print(self.bestsellers_line)
        current_user = Users.objects.get(username=request.user)
        total_amount = current_user.total_amount_of_orders
        total_amount_all_percent = 0
        sale = current_user.discount_percentage + 1
        try:
            orders_history = Orders.objects.filter(recipient=request.user).order_by('id')[0]
            product_quantity = Order_Items.objects.filter(order__id=orders_history.id)
        except:
            orders_history = None
            product_quantity = None

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
            'add_to_cart': self.add_to_cart,
            'orders_history': orders_history,
            'products': product_quantity,
            'all_products': self.all_products,
            'brands': self.brands,
            'contact_form': self.contact_form,
            'bestsellers_line': self.bestsellers_line,
        }
        return render(
            request,
            'users_lk.html',
            context=context
        )

    def post(self, request, product_id, *args, **kwargs):

        user = Users.objects.get(username=request.user)
        current_user = Users.objects.get(username=request.user)
        total_amount = current_user.total_amount_of_orders
        total_amount_all_percent = 0
        sale = current_user.discount_percentage + 1
        try:
            orders_history = Orders.objects.filter(recipient=request.user).order_by('id')[0]
            product_quantity = Order_Items.objects.filter(order__id=orders_history.id)
        except:
            orders_history = None
            product_quantity = None

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
            'add_to_cart': self.add_to_cart,
            'orders_history': orders_history,
            'products': product_quantity,
            'all_products': self.all_products,
            'brands': self.brands,
            'contact_form': self.contact_form,
            'bestsellers_line': self.bestsellers_line,
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
                Delivery_Addresses.objects.update(
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

        return render(
            request,
            'users_lk.html',
            context=context
        )


class Catalog_Item(View):

    def get(self, request, title, slug, *args, **kwargs):
        
        product = get_object_or_404(Product, title=title, slug=slug)
        all_products_first = Product.objects.filter(brand=product.brand)[:4]
        all_products_last = Product.objects.filter(brand=product.brand)[4:]
        product_images = Product_Images.objects.filter(product=product)
        
        context = {
            'product': product,
            'product_images': product_images,
            'get_price': Get_Price_Form(),
            'all_products_first': all_products_first,
            'all_products_last': all_products_last,
        }
        
        return render(request, 'catalog_item.html', context=context)

    def post(self, request, title, slug, *args, **kwargs):
        
        product = get_object_or_404(Product, title=title, slug=slug)
        product_images = Product_Images.objects.filter(product=product)
        form = Get_Price_Form(request.POST)
        all_products = Product.objects.filter(brand=product.brand)

        context = {
            'product': product,
            'product_images': product_images,
            'get_price': Get_Price_Form(),
            'all_products': all_products,
        }
       
        if form.is_valid():
            telephone_number = form.cleaned_data['telephone_number']
            email = form.cleaned_data['email']
            contact_name = form.cleaned_data['contact_name']
            company_name = form.cleaned_data['company_name']
            try:
                send_mail(
                    'Прайс Beauty Force',
                    'Добрый день {}! \n Запрошенный прайс во вложении.'.format(
                        contact_name,
                    ),
                    'reg@beforce.ru',
                    [email],
                    fail_silently=False,
                )
                
                send_mail(
                    'Заказ выгрузки прайса',
                    'Контактное лицо {}, телефон {}, компания {}'.format(
                        contact_name,
                        telephone_number,
                        company_name
                    ),
                    'reg@beforce.ru',
                    ['reg@beforce.ru'],
                    fail_silently=False,
                )
                messages.success(request, "price")
            except:
                messages.error(request, "Что-то пошло не так, попробуйте снова.")
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


class Add_To_Cart(View):

    def post(self, request, product_id, *args, **kwargs):
        cart = Cart_Mixin(request)
        product = get_object_or_404(Product, id=product_id)
        form = Add_To_Cart_Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['quantity'] > product.stock:
                response = 'Извините, доступное количество товара для заказа {}'.format(product.stock)
                return HttpResponse(simplejson.dumps({
                    'response': response,
                    'result': 'error',
                    'product_id': product_id
                }), content_type='application/json')
            else:
                cart.add(product=product,
                         quantity=cd['quantity'],
                         update_quantity=cd['update'])
                return HttpResponse(simplejson.dumps({'result': 'success'}))


class Delete_From_Cart(View):

    def get(self, request, product_id, *args, **kwargs):
        cart = Cart_Mixin(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return HttpResponseRedirect('/basket/')

    def post(self, request, product_id, *args, **kwargs):
        cart = Cart_Mixin(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return HttpResponseRedirect('/basket/')


class Contact_Us(View):

    def post(self, request, *args, **kwargs):
        form = Contact_Form(request.POST)
        if form.is_valid():
            try:
                send_mail(
                    'Заказ звонка на консультацию',
                    'Контактное лицо {}, телефон {}'.format(
                        form.cleaned_data['name'],
                        form.cleaned_data['telephone_number'],
                    ),
                    'reg@beforce.ru',
                    ['reg@beforce.ru'],
                    fail_silently=False,
                )
                response = "Мы приняли Вашу заявку, скоро с Вами свяжется наш специалист"
                return HttpResponse(simplejson.dumps({'result': 'success', 'response': response}))
            except:
                response = "Что-то пошло не так, попробуйте позднее"
                return HttpResponse(simplejson.dumps({'result': 'error', 'response': response}))


class Basket_Page(View):

    def get(self, request, *args, **kwargs):
        delivery = Delivery_Addresses.objects.get(recipient=request.user)
        cart = Cart_Mixin(request)
        sale = cart.get_total_price() - (cart.get_total_price() * (100 - delivery.recipient.discount_percentage)/100)
        if not cart:
            cart = None
            total_and_delivery_sum = 0
        else:
            total_and_delivery_sum = delivery.delivery + (cart.get_total_price() * (100 - delivery.recipient.discount_percentage)/100)

        context = {
            'cart': cart,
            'delivery': delivery,
            'total_and_delivery_sum': total_and_delivery_sum,
            'sale': sale,
        }

        return render(request, 'basket.html', context=context)

    def post(self, request, *args, **kwargs):
        cart = Cart_Mixin(request)
        recipient = request.user
        address = Delivery_Addresses.objects.get(recipient=recipient)
        product = Product.objects.all()
        total_and_delivery_sum = cart.get_total_price() * (100 - address.recipient.discount_percentage) / 100
        try:
            order = Orders.objects.create(
                recipient=recipient,
                address=address,
                order_sum=total_and_delivery_sum,
                delivery=address.delivery
            )
            order.save()

            for item in cart:
                Order_Items.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            for products in product:
                for product_item in cart:
                    if products.pk == product_item['product'].pk:
                        print(products)
                        products.stock = products.stock - product_item['quantity']
                        products.save()
            send_mail(
                'Заказ №{}'.format(order.id),
                'Заказчик {}, телефон заказчика {}'.format(
                    recipient,
                    order.recipient.phoneNumber,
                ),
                'reg@beforce.ru',
                ['reg@beforce.ru'],
                fail_silently=False,
            )
            cart.clear()
        except:
            messages.error(request, "Заказ не сформирован, попробуйте снова")
            return HttpResponseRedirect('/basket/')
        messages.success(request, "1")
        return HttpResponseRedirect('/basket/')


class Users_Orders_History(View):
    success_message = 'Вам на почту отправлена ссылка на изменение пароля'
    error_message = 'Что-то пошло не так, письмо не было отправлено'

    success_message_add_adresses = "Адрес доставки успешно добавлен"
    error_message_add_adresses = "Что-то пошло не так, пожалуйста, попробуйте снова"

    def get(self, request, *args, **kwargs):

        products = []
        orders_history = Orders.objects.filter(recipient=request.user)
        if not orders_history:
            orders_history = None
        else:
            for i in orders_history:
                product_quantity = Order_Items.objects.filter(order__id=i.id)
                products.append(product_quantity)
        context = {
            'orders_history': orders_history,
            'products': products,
        }

        return render(request, 'user_history_orders.html', context=context)

    def post(self, request, *args, **kwargs):

        products = []
        orders_history = Orders.objects.filter(recipient=request.user)
        if not orders_history:
            orders_history = None
        else:
            for i in orders_history:
                product_quantity = Order_Items.objects.filter(order__id=i.id)
                products.append(product_quantity)
        context = {
            'orders_history': orders_history,
            'products': products,
        }

        if request.POST.get('change_name'):
            try:
                username = Users.objects.get(username=request.user)
                username.username = request.POST.get('change_name')
                username.save()
                messages.success(request, 'Вы успешно сменили имя')
                return HttpResponseRedirect('/personal_account/orders_history/')

            except:
                messages.error(request, 'Что-то пошло не так, попробуйте снова')

        elif request.POST.get('acсount-email'):

            mail = request.POST.get('acсount-email')
            message = render_to_string('password_reset_email.html', {
                'user': request.user,
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
            delivery_addresses = Delivery_Addresses.objects.get(recipient=request.user)
            if not delivery_addresses:
                try:
                    Delivery_Addresses.objects.create(
                        recipient=request.user,
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
            else:
                try:
                    delivery_addresses.recipient = request.user
                    delivery_addresses.city = city
                    delivery_addresses.street = street
                    delivery_addresses.home = home
                    delivery_addresses.entrance = entrance
                    delivery_addresses.floor = floor
                    delivery_addresses.apartment_or_office = apartment_or_office
                    delivery_addresses.save()
                    messages.success(request, self.success_message_add_adresses)
                except:
                    messages.error(request, self.error_message_add_adresses)

        return render(request, 'user_history_orders.html', context=context)


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
