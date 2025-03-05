import datetime
from smtplib import SMTPException
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import ClientModel, MessageModel, MailingModel, MailingAttemptModel
from .forms import StyleFormMixin
import os
from dotenv import load_dotenv

load_dotenv()

class ClientView(ListView):
    model = ClientModel

class ClientDetail(DetailView):
    model = ClientModel


class ClientCreate(StyleFormMixin, CreateView):
    model = ClientModel
    fields = ["full_name", "email", "note"]
    success_url = reverse_lazy("web_mailing:clients_list")



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


class MessageDetail(DetailView):
    model = MessageModel



class MessageCreate(StyleFormMixin, CreateView):
    model = MessageModel
    fields = ["title", "text"]
    success_url = reverse_lazy("web_mailing:messages_list")


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

class MailingCreate(StyleFormMixin, CreateView):
    model = MailingModel
    fields = ["message", "recipients"]
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



