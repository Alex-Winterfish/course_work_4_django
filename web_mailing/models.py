from django.db import models
from users.models import CustomUser


class ClientModel(models.Model):
    '''Модель получателя рассылки'''
    email = models.EmailField(max_length=100, verbose_name="Электронная почта", unique=True)
    full_name = models.CharField(max_length=100, verbose_name="Ф.И.О")
    note = models.TextField(max_length=1000, verbose_name="Комментарий")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="users_client", verbose_name="клиент пользователя", null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["full_name"]
        permissions = [
            ("can_view_client", "can view client"),
        ]


class MessageModel(models.Model):
    '''Модель сообщения'''
    title = models.CharField(max_length=100, verbose_name="тема письма")
    text = models.TextField(max_length=1000, verbose_name="тест письма")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="users_message", verbose_name="сообщения пользователя", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["title"]
        permissions = [
            ("can_view_message", "can view message"),
        ]


class MailingModel(models.Model):
    '''Модель рассылки'''
    CREATED = "Создана"
    STARTED = "Начата"
    ENDED = "Окончена"

    STATUS_IN_CHOICES = [
        (CREATED, "Создана"),
        (STARTED, "Начата"),
        (ENDED, "Окончена"),
    ]

    start = models.DateTimeField(null=True, verbose_name="дата и время первой отправки")
    end = models.DateTimeField(null=True, verbose_name="дата и время окончания отправки")
    status = models.CharField(choices=STATUS_IN_CHOICES, default=CREATED, verbose_name="статус рассылки")
    message = models.ForeignKey(MessageModel, on_delete=models.CASCADE, verbose_name="сообщения для отправки")
    recipients = models.ManyToManyField(ClientModel, verbose_name="получатели")
    owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="создатель рассылки")

    def __str__(self):
        return f"{self.message}. Статус: {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["start", "end"]
        permissions = [
            ("can_view_mailing", "can view mailing"),
            ("can_disable_mailing", "can disable mailing")
        ]


class MailingAttemptModel(models.Model):
    '''Модель попытка рассылки'''
    SUCCESS = "Успешно"
    FAIL = "Не успешно"

    STATUS_IN_CHOICES = [
        (SUCCESS, "Успешно"),
        (FAIL, "Не успешно"),
    ]


    attempt_start = models.DateTimeField(auto_now=True, verbose_name="дата и время попытки")
    status = models.CharField(choices=STATUS_IN_CHOICES, verbose_name="статус попытки")
    server_feedback = models.CharField(max_length=500, verbose_name="ответ почтового сервера")
    mailing = models.ForeignKey(MailingModel, on_delete=models.CASCADE, verbose_name="рассылка")
    owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE,
                              verbose_name="Попытка рассылки пользователя")

    def __str__(self):
        return f"{self.mailing} статус: {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["attempt_start"]



