from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.urls import reverse

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
    recipient = models.ForeignKey('Users', on_delete=models.CASCADE, null=True, blank=True, unique=False,
                                  verbose_name='Заказчик')
    city = models.CharField(max_length=100, null=True, verbose_name='Город')
    street = models.CharField(max_length=100, null=True, verbose_name='Улица')
    home = models.CharField(max_length=100, null=True, verbose_name='Номер дома')
    entrance = models.CharField(max_length=100, null=True, verbose_name='Номер подъезда')
    floor = models.CharField(max_length=100, null=True, verbose_name='Этаж')
    apartment_or_office = models.CharField(max_length=100, null=True, verbose_name='Номер квартиры/Офиса')

    def __str__(self):
        return f'{self.city}'

    class Meta:
        verbose_name = "Адреса доставки"
        verbose_name_plural = "Адреса доставки"


"""
Название бренда
"""


class Brands(models.Model):
    brand_name = models.CharField(max_length=100, null=True, verbose_name='Название бренда')

    def __str__(self):
        return f'{self.brand_name}'

    class Meta:
        verbose_name = "Бренды"
        verbose_name_plural = "Бренды"


"""
Категория товара
"""


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Категория товара')
    slug = models.SlugField(unique=True, null=True, verbose_name='Ссылка')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товара"


"""
Товар
"""


class Product(models.Model):
    brand = models.ForeignKey('Brands', on_delete=models.CASCADE, null=True, blank=True, unique=False,
                              verbose_name='Название бренда')
    title = models.CharField(max_length=50, null=True, verbose_name='Название товара')
    about = models.TextField(max_length=1000, null=True, verbose_name='Описание')
    image = models.ImageField(blank=True, upload_to='images/product_photo/', verbose_name='Фото товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток товара')
    available = models.BooleanField(default=True, verbose_name='Доступность товара')
    slug = models.SlugField(unique=True, null=True, verbose_name='Ссылка')
    vendor_code = models.CharField(max_length=50, null=True, verbose_name='Артикул')
    barcode = models.IntegerField(default=0, null=True, verbose_name='Штрихкод')
    mode_of_application = models.TextField(max_length=1000, null=True, verbose_name='Способ применения')
    compound = models.TextField(max_length=1000, null=True, verbose_name='Состав')
    precautionary_measures = models.TextField(max_length=1000, null=True, verbose_name='Меры предосторожности')

    def get_absolute_url(self):
        return reverse('catalog_item',
                       args=[self.slug, self.title])

    def __str__(self):
        return f'{self.title}'

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
    customer = models.ForeignKey('Users', on_delete=models.CASCADE, null=True, blank=True, unique=False,
                                 verbose_name='Заказчик')
    date = models.DateField(verbose_name='Дата доставки')
    address = models.ForeignKey('Delivery_Addresses', on_delete=models.CASCADE, null=True, blank=True, unique=False,
                                verbose_name='Адрес доставки')
    online_or_offline = models.PositiveSmallIntegerField(choices=PURCHASE_CHOICES, blank=True, null=True, default=0,
                                                         verbose_name='Онлайн/Оффлайн')
    number_card = models.IntegerField(default=0, null=True, verbose_name='Номер карты')
    purchase_amount = models.IntegerField(default=0, null=True, verbose_name='Сумма покупки')
    delivery = models.IntegerField(default=0, null=True, verbose_name='Сумма доставки')
    product = models.ManyToManyField(Product, blank=True, verbose_name='Товар')
    total_products = models.PositiveIntegerField(default=0, verbose_name='Количество товара')

    def __str__(self):
        return f'{self.address}'

    class Meta:
        verbose_name = "История заказов"
        verbose_name_plural = "История заказов"
