from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime
from web_mailing.models import MessageModel, MailingModel, MailingAttemptModel, ClientModel
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "class for mailing attempts"

    def handle(self, *args, **options):

        clients = ClientModel.objects.all()
        messages = MessageModel.objects.all()
        mailing = MailingModel.objects.all()
        clients_list = list()
        for client in clients:
            clients_list.append(client)
            for message in messages:
                try:

                    send_mail(
                        subject=message.title,
                        message=message.text,
                        from_email='alksbulgakov@gmail.com',
                        recipient_list=[client.email],
                    )

                    self.save_mailing(message, clients_list, success="Успешно")
                    self.save_attempt(mailing, success="Успешно", response='Message sent successfully')


                except Exception as e:
                    self.save_mailing(message, clients_list, success="Не успешно")
                    self.save_attempt(mailing, success="Не успешно", response=str(e))


    def save_attempt(self, mailing, success, response):
        with transaction.atomic():
            attempt = MailingAttemptModel(
                mailing=mailing,
                status=success,
                server_feedback=response
            )
            attempt.save()

    def save_mailing(self, message, client, success=None):

        with transaction.atomic():
            mailing = MailingModel(
                end=datetime.now(),
                status=success,
                message=message,
                recipients=client
            )
            mailing.save()