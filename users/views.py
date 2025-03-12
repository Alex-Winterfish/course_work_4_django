# -*- coding: utf-8 -*-
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView, TemplateView
from web_mailing.forms import StyleFormMixin
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
import os
from dotenv import load_dotenv

from .models import CustomUser

load_dotenv()

class RegisterView(StyleFormMixin, CreateView):  #изменить для отправки подтверждения регистрации через почту
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:user_register")


    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        login(self.request, user)
        self.send_welcome_email(user.email, user.id)
        return super().form_valid(form)

    def send_welcome_email(self, user_email, user_id):
        subject = "Добро пожаловать в наш сервис"
        message = f"Спасибо, что зарегистрировались в нашем сервисе! Для завершения регистрации перейдите по ссылке: http://127.0.0.1:8000/users/user_confirm/{user_id}/"
        from_email = os.getenv("EMAIL_HOST_USER")
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class CustomLoginView(StyleFormMixin, LoginView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CustomUserView(ListView):
    model = CustomUser
    template_name = 'customuser_list.html'


def user_block(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    user.is_active = not user.is_active
    user.save()

    return redirect('users:users_list')

class CustomUserDetail(DetailView):
    model = CustomUser
    template_name = "customuser_detail.html"

class CustomUserUpdate(StyleFormMixin, UpdateView):
    model = CustomUser
    fields = ["avatar", "phone", "email", "country", "is_active"]
    template_name = "customuser_form.html"
    def get_success_url(self):
        return reverse_lazy('users:user_detail', kwargs={'pk': self.object.pk})

class CustomUserRegister(TemplateView):
    template_name = "user_register.html"

def user_confirm(request, pk):
    '''Функция для подтверждения регистрации'''
    user = get_object_or_404(CustomUser, id=pk)
    user.is_active = True
    user.save()
    login(request, user)

    return redirect('web_mailing:main')



