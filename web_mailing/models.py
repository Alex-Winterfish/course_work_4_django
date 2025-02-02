from django.db import models


class ClientModel(models.Model):
    '''Модель получателя рассылки'''
    email = models.EmailField(max_length=100, verbose_name="Электронная почта", unique=True)
    full_name = models.CharField(max_length=100, verbose_name="Ф.И.О")
    note = models.TextField(max_length=1000, verbose_name="Комментарий")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["full_name"]


class MessageModel(models.Model):
    '''Модель сообщения'''
    title = models.CharField(max_length=100, verbose_name="тема письма")
    text = models.TextField(max_length=1000, verbose_name="тест письма")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["title"]


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

    start = models.DateTimeField(auto_now_add=True, verbose_name="дата и время первой отправки")
    end = models.DateTimeField(verbose_name="дата и время окончания отправки")
    status = models.CharField(choices=STATUS_IN_CHOICES, verbose_name="статус рассылки")
    message = models.ForeignKey(MessageModel, on_delete=models.CASCADE, verbose_name="сообщения для отправки")
    recipients = models.ManyToManyField(ClientModel, verbose_name="получатели")

    def __str__(self):
        return f"{self.message} статус: {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["start", "end"]


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
    server_feedback = models.CharField(max_length=100, verbose_name="ответ почтового сервера")
    mailing = models.ForeignKey(MailingModel, on_delete=models.CASCADE, verbose_name="рассылка")

    def __str__(self):
        return f"{self.mailing} статус: {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["attempt_start"]



