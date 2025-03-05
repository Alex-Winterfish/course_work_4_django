# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", null=True, blank=True)
    phone = models.CharField(max_length=35, verbose_name="Phone", null=True, blank=True,
                             help_text="Введите номер телефона")
    country = models.CharField(max_length=50, verbose_name="Страна", help_text="Введите страну")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

