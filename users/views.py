# -*- coding: utf-8 -*-
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from web_mailing.forms import StyleFormMixin
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
import os
from dotenv import load_dotenv

load_dotenv()

class RegisterView(StyleFormMixin, CreateView):  #изменить для отправки подтверждения регистрации через почту
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("web_mailing:client_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать в наш сервис"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        from_email = os.getenv("EMAIL_HOST_USER")
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class CustomLoginView(StyleFormMixin, LoginView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




