import datetime
from smtplib import SMTPException
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import ClientModel, MessageModel, MailingModel, MailingAttemptModel
from .forms import StyleFormMixin, MailingForm
import os
from dotenv import load_dotenv

load_dotenv()

class ClientView(ListView):
    model = ClientModel

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and not user.groups.filter(name='managers').exists():
            return ClientModel.objects.filter(owner=user)
        elif user.groups.filter(name='managers').exists():
            return ClientModel.objects.all()
        return super().get_queryset()


class ClientDetail(DetailView):
    model = ClientModel


class ClientCreate(StyleFormMixin, CreateView):
    model = ClientModel
    fields = ["full_name", "email", "note"]
    success_url = reverse_lazy("web_mailing:clients_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)



class ClientUpdate(StyleFormMixin, UpdateView):
    model = ClientModel
    fields = ["full_name", "note", "email"]
    def get_success_url(self):
        return reverse_lazy('web_mailing:client_detail', kwargs={'pk': self.object.pk})

class ClientDelite(DeleteView):
    model = ClientModel
    success_url = reverse_lazy('web_mailing:clients_list')


class MessageView(ListView):
    model = MessageModel
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and not user.groups.filter(name='managers').exists():
            return MessageModel.objects.filter(owner=user)
        elif user.groups.filter(name='managers').exists():
            return MessageModel.objects.all()
        return super().get_queryset()


class MessageDetail(DetailView):
    model = MessageModel



class MessageCreate(StyleFormMixin, CreateView):
    model = MessageModel
    fields = ["title", "text"]
    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)
    success_url = reverse_lazy("web_mailing:messages_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class MessageUpdate(StyleFormMixin, UpdateView):
    model = MessageModel
    fields = ["title", "text"]
    def get_success_url(self):
        return reverse_lazy('web_mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageDelete(DeleteView):
    model = MessageModel
    success_url = reverse_lazy("web_mailing:messages_list")

class MailingView(ListView):
    model = MailingModel
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and not user.groups.filter(name='managers').exists():
            return MailingModel.objects.filter(owner=user)
        elif user.groups.filter(name='managers').exists():
            return MailingModel.objects.all()
        return super().get_queryset()

class MailingCreate(StyleFormMixin, CreateView):
    model = MailingModel
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('web_mailing:mailing_list')


class MailingUpdate(StyleFormMixin, UpdateView):
    model = MailingModel
    fields = ["status", "message", "recipients"]
    success_url = reverse_lazy('web_mailing:mailing_list')


class MailingDetail(StyleFormMixin, DetailView):
    model = MailingModel


class MailingDelete(DeleteView):
    model = MailingModel
    success_url = reverse_lazy('web_mailing:mailing_list')


class MailingAttemptView(ListView):
    model = MailingAttemptModel


class MailingAttemptCreate(StyleFormMixin, CreateView):
    model = MailingAttemptModel
    fields = ["mailing"]

    def send_email(self, user_email, subject, message):
        from_email = os.getenv("EMAIL_HOST_USER")
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)



    def form_valid(self, form):

        subject = form.instance.mailing.message.title
        message = form.instance.mailing.message.text
        recipients = form.instance.mailing.recipients
        mailing = MailingModel.objects.get(id=form.instance.mailing.id) #получаем объект рассылки для изменеия статуса
        mailing.status = "Начата"
        mailing.save()
        mailing.start = datetime.datetime.now()

        for recipient in recipients.all():
            try:
                mailing_attempt = MailingAttemptModel(mailing=form.instance.mailing)
                self.send_email(recipient.email, subject, message,)
                mailing_attempt.attempt_start = datetime.datetime.now()
                mailing_attempt.status = "Успешно"
                mailing_attempt.save()

            except SMTPException as e:
                mailing_attempt = MailingAttemptModel(mailing=form.instance.mailing)
                self.send_email(recipient.email, subject, message, )
                mailing_attempt.attempt_start = datetime.datetime.now()
                mailing_attempt.status = "Не успешно"
                mailing_attempt.server_feedback = e
                mailing_attempt.save()

        mailing.status = "Окончена"
        mailing.end = datetime.datetime.now()
        mailing.save()

        return super().form_valid(form)

    success_url = reverse_lazy("web_mailing:mailing_attempt")



