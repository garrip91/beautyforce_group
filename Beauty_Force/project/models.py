from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal

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
    index = models.CharField(max_length=100, null=True, verbose_name='Индекс')
    delivery = models.IntegerField(default=0, null=True, verbose_name='Сумма доставки')

    def __str__(self):
        return str("Заказчик: {0}, Город: {1}, Улица: {2}".format(
            self.recipient, self.city, self.street)
        )

    class Meta:
        verbose_name = "Адреса доставки"
        verbose_name_plural = "Адреса доставки"


"""

Название бренда

"""


class Brands(models.Model):
    brand_name = models.CharField(max_length=100, null=True, verbose_name='Название бренда', unique=True)
    brand_image = models.ImageField(blank=True, upload_to='images/brand/', verbose_name='Картинка бренда')
    tagline = models.CharField(max_length=100, null=True, verbose_name='Слоган')
    country = models.CharField(max_length=100, null=True, verbose_name='Страна производитель')
    assortment = models.CharField(max_length=100, null=True, verbose_name='Ассортимент')
    category = models.CharField(max_length=100, null=True, verbose_name='Категория')
    price_segment = models.CharField(max_length=100, null=True, verbose_name='Ценовой сегмент')
    description = models.CharField(max_length=100, null=True, verbose_name='Описание')
    reviews = models.CharField(max_length=100, null=True, verbose_name='Состав и ингредиенты')
    video = models.FileField(upload_to='videos/brands/', null=True, verbose_name="Видео")

    def __str__(self):
        return str(self.brand_name)

    class Meta:
        verbose_name = "Бренды"
        verbose_name_plural = "Бренды"


"""

Категории брендов

"""


class Brands_Category(models.Model):
    brand = models.ForeignKey(Brands, related_name='brand_category', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Бренд')
    category = models.CharField(max_length=100, null=True, verbose_name='Категория бренда')
    description = models.CharField(max_length=1000, null=True, verbose_name='Описание')

    def __str__(self):
        return str(self.brand)

    class Meta:
        verbose_name = "Категории брендов"
        verbose_name_plural = "Категории брендов"


"""

Преимущества бренда

"""


class Brand_Benefits(models.Model):
    brand = models.ForeignKey(Brands, related_name='brand_benefits', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Бренд')
    title = models.CharField(max_length=100, null=True, verbose_name='Заголовок')
    description = models.CharField(max_length=1000, null=True, verbose_name='Описание')

    def __str__(self):
        return str(self.brand)

    class Meta:
        verbose_name = "Преимущества бренда"
        verbose_name_plural = "Преимущества бренда"


"""

Состав и ингредиенты

"""


class Compound_And_Ingredients(models.Model):
    brand = models.ForeignKey(Brands, related_name='brand_compound', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Бренд')
    component = models.CharField(max_length=100, null=True, verbose_name='Компонент')
    description = models.CharField(max_length=1000, null=True, verbose_name='Описание')

    def __str__(self):
        return str(self.brand)

    class Meta:
        verbose_name = "Состав и компоненты бренда"
        verbose_name_plural = "Состав и компоненты бренда"


"""

Отзывы бренда

"""


class Reviews(models.Model):
    brand = models.ForeignKey(Brands, related_name='brand_reviews', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Бренд')
    name = models.CharField(max_length=100, null=True, verbose_name='Имя покупателя')
    review = models.TextField(max_length=1000, null=True, verbose_name='Отзыв')
    grade = models.IntegerField(default=0, null=True, verbose_name='Оценка')

    def __str__(self):
        return str(self.brand)

    class Meta:
        verbose_name = "Отзывы о бренде"
        verbose_name_plural = "Отзывы о бренде"


"""

Линейки бестселлеров

"""


class Bestsellers_Line(models.Model):
    line = models.CharField(max_length=200, verbose_name='Линейки бестселлеров')

    def __str__(self):
        return str(self.line)

    class Meta:
        verbose_name = "Линейки бестселлеров"
        verbose_name_plural = "Линейки бестселлеров"


"""

Товары

"""


# , to_field='brand_name', db_column='brand'

class Product(models.Model):
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, null=True, blank=True, unique=False,
                              verbose_name='Название бренда')
    title = models.CharField(max_length=1000, null=True, verbose_name='Название товара')
    about = models.TextField(max_length=1000, null=True, verbose_name='Описание')
    hidden_description = models.TextField(max_length=1000, null=True, verbose_name='Скрытое описание')
    image_for_cart = models.ImageField(blank=True, upload_to='images/product_photo/',
                                       verbose_name='Картинка для корзины')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Оптовая цена')
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Розничная цена')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток товара')
    available = models.BooleanField(default=True, verbose_name='Доступность товара')
    slug = models.SlugField(unique=True, null=True, verbose_name='Ссылка', blank=True)
    article = models.CharField(max_length=50, null=True, verbose_name='Артикул')
    barcode = models.IntegerField(default=0, null=True, verbose_name='Штрихкод')
    mode_of_application = models.TextField(max_length=1000, null=True, verbose_name='Способ применения')
    compound = models.TextField(max_length=1000, null=True, verbose_name='Состав')
    precautionary_measures = models.TextField(max_length=1000, null=True, verbose_name='Меры предосторожности',
                                              blank=True)
    product_line = models.ForeignKey('Bestsellers_Line', on_delete=models.CASCADE, null=True, blank=True,
                                     unique=False,
                                     verbose_name='Товарная группа')
    supplier = models.CharField(max_length=100, null=True, verbose_name='Поставщик')
    country = models.CharField(max_length=100, null=True, verbose_name='Страна')
    shelf_life = models.CharField(max_length=100, null=True, verbose_name='Срок годности')
    weight_brutto = models.CharField(max_length=100, null=True, verbose_name='Вес брутто')

    def get_absolute_url(self):
        return reverse('catalog_item',
                       args=[self.slug, self.title])

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


"""

Заказы

"""


class Orders(models.Model):
    STATUS_NEW = 'Новый заказ'
    STATUS_IN_PROGRESS = 'Обрабатывается складом'
    STATUS_READY = 'Передан в доставку'
    STATUS_COMPLETED = 'Доставлен'

    BUYING_TYPE_SELF = 'Онлайн'
    BUYING_TYPE_DELIVERY = 'Оффлайн'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Обрабатывается складом'),
        (STATUS_READY, 'Передан в доставку'),
        (STATUS_COMPLETED, 'Доставлен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Онлайн'),
        (BUYING_TYPE_DELIVERY, 'Оффлайн')
    )

    recipient = models.ForeignKey('Users', on_delete=models.CASCADE, null=True, blank=True, unique=False,
                                  verbose_name='Заказчик')
    address = models.ForeignKey('Delivery_Addresses', on_delete=models.CASCADE, null=True, blank=True, unique=False,
                                verbose_name='Адрес доставки')
    paid = models.BooleanField(default=False, verbose_name='Статус оплаты')
    number_card = models.IntegerField(default=0, null=True, verbose_name='Номер карты')
    delivery = models.IntegerField(default=0, null=True, verbose_name='Сумма доставки')
    order_sum = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name='Цена с учетом скидки')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str("Заказ №{}".format(self.id))

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def masking_cart(self):
        return str(self.number_card)[-4:].rjust(len(str(self.number_card)), "*")

    def total_amount(self):
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'


"""

Заказы(Количество товара и тд)

"""


class Order_Items(models.Model):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'


"""

Изображения для товара

"""


class Product_Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Товар')
    image = models.ImageField(blank=True, upload_to='images/product_photo/', verbose_name='Фото товара')

    class Meta:
        verbose_name = 'Картинки товара'
        verbose_name_plural = 'Картинки товара'


"""

Пресса

"""


class Press(models.Model):
    logo = models.ImageField(blank=True, upload_to='images/press/logo/', verbose_name='Лого')
    title = models.CharField(max_length=100, null=True, verbose_name='Заголовок')
    text = models.CharField(max_length=200, null=True, verbose_name='Текст статитьи', blank=True)
    image = models.ImageField(blank=True, upload_to='images/press/image/', verbose_name='Фото статьи')
    link = models.URLField(verbose_name='Ссылка на статью', null=True, blank=True)
    date = models.DateField(verbose_name='Дата публикации', default=timezone.now)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'
