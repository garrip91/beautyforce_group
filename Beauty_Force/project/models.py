from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

"""
Пользователи
"""


class Users(AbstractUser):
    developer = 0
    admin = 1
    manager = 2
    client = 3
    ROLE_CHOICES = (
        (developer, 'Разработчик'),
        (admin, 'Администратор'),
        (manager, 'Менеджер'),
        (client, 'Клиент'),
    )
    inn = models.IntegerField(default=0, unique=True, null=False, verbose_name='ИНН')
    email = models.EmailField(blank=True, unique=True, null=False, verbose_name='Email')
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, default=0,
                                   verbose_name='Телефон')
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3, verbose_name='Роль')
    discount_percentage = models.IntegerField(default=0, null=True, verbose_name='Песональная скидка')
    total_amount_of_orders = models.IntegerField(default=0, null=True, verbose_name='Общая сумма покупок')

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"


"""
Адреса доставки пользователей 
"""


class Delivery_Addresses(models.Model):
    recipient = models.ForeignKey('Users', on_delete=models.CASCADE, null=True, blank=True, unique=False)
    city = models.CharField(max_length=100, null=True, verbose_name='Город')
    street = models.CharField(max_length=100, null=True, verbose_name='Улица')
    home = models.CharField(max_length=100, null=True, verbose_name='Номер дома')
    entrance = models.CharField(max_length=100, null=True, verbose_name='Номер подъезда')
    floor = models.CharField(max_length=100, null=True, verbose_name='Этаж')
    apartment_or_office = models.CharField(max_length=100, null=True, verbose_name='Номер квартиры/Офиса')

    class Meta:
        verbose_name = "Адреса доставки"
        verbose_name_plural = "Адреса доставки"


"""
Название бренда
"""


class Brands(models.Model):
    brand_name = models.CharField(max_length=100, null=True, verbose_name='Название бренда')

    class Meta:
        verbose_name = "Бренды"
        verbose_name_plural = "Бренды"


"""
Товар
"""


class Product(models.Model):
    brand = models.ForeignKey('Brands', on_delete=models.CASCADE, null=True, blank=True, unique=False,
                              verbose_name='Название бренда')
    about = models.TextField(max_length=1000, null=True, verbose_name='Описание')
    image = models.ImageField(blank=True, upload_to='images/product_photo/', verbose_name='Фото товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


"""
История заказов
"""


class Purchase_History(models.Model):
    online = 0
    offline = 1

    PURCHASE_CHOICES = (
        (online, 'Онлайн покупка'),
        (offline, 'Оффлайн покупка'),
    )
    customer = models.ForeignKey('Users', on_delete=models.CASCADE, null=True, blank=True, unique=False)
    date = models.DateField(verbose_name='Дата доставки')
    address = models.CharField(max_length=100, null=True, verbose_name='Адрес доставки')
    online_or_offline = models.PositiveSmallIntegerField(choices=PURCHASE_CHOICES, blank=True, null=True, default=0,
                                                         verbose_name='Онлайн/Оффлайн')
    number_card = models.IntegerField(default=0, null=True, verbose_name='Номер карты')
    purchase_amount = models.IntegerField(default=0, null=True, verbose_name='Сумма покупки')
    delivery = models.IntegerField(default=0, null=True, verbose_name='Сумма доставки')
    product = models.ManyToManyField(Product, blank=True, verbose_name='Товар')
    total_products = models.PositiveIntegerField(default=0, verbose_name='Количество товара')

    class Meta:
        verbose_name = "История заказов"
        verbose_name_plural = "История заказов"
