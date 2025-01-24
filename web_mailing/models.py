from django.db import models

class ClientModel(models.Model):
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
    title = models.CharField(max_length=100, verbose_name="тема письма")
    text = models.TextField(max_length=1000, verbose_name="тест письма")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["title"]
