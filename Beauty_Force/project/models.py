from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


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
    inn = models.IntegerField(default=0, unique=True, null=False)
    email = models.EmailField(blank=True, unique=True, null=False)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, default=0)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)