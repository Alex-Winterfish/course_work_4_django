from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime

from users.models import CustomUser
from web_mailing.models import MessageModel, MailingModel, MailingAttemptModel, ClientModel
from django.core.mail import send_mail
import os
from dotenv import load_dotenv
load_dotenv()


class Command(BaseCommand):
    help = "class for mailing attempts"


    @staticmethod
    def user_mailings(users):
        '''Метод для выбора пользователя'''
        print('От кого начать рассылку?:')
        users_dict = dict()
        for i in range(len(users)):
            users_dict[i+1] = users[i]
            print(f'введите {i+1} для {users[i].email}')

        user = int(input("Выберите пользователя: "))
        return users_dict[user]

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.filter(is_staff=False) #Получаем пользователей


        user = self.user_mailings(users)

        while not MailingModel.objects.filter(owner=user):
            print('\nРассылки отсутствуют. Выберите другого пользователя')
            user = self.user_mailings(users)

        mailings = MailingModel.objects.filter(owner=user)

        print('\nКакую рассылку начать?: ')
        mailings_dict = dict()

        for i in range(len(mailings)):
            mailings_dict[i + 1] = mailings[i]
            print(f'введите {i + 1} рассылки {mailings[i]}')

        user_input = int(input("Выберите рассылку: "))

        mailing_instance = mailings_dict[user_input]

        from_email = os.getenv('EMAIL_HOST_USER')
        subject = mailing_instance.message.title
        message = mailing_instance.message.text
        recipients = mailing_instance.recipients
        mailing_instance.status = "Начата"
        mailing_instance.save()

        mailing_instance.start = datetime.now()

        for recipient in recipients.all():
            mailing_attempt = MailingAttemptModel(mailing=mailing_instance)
            mailing_attempt.attempt_start = datetime.now()
            try:
                send_mail(subject, message, from_email, [recipient.email], fail_silently=False)
                mailing_attempt.status = "Успешно"
                mailing_attempt.owner = user
                mailing_attempt.save()

            except Exception as e:

                mailing_attempt.status = "Не успешно"
                mailing_attempt.server_feedback = e
                mailing_attempt.owner = user
                mailing_attempt.save()

        mailing_instance.status = "Окончена"
        mailing_instance.end = datetime.now()
        mailing_instance.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Выполнена рассылка: {mailing_instance} \n"
                f"Начата: {mailing_instance.start} \n"
                f"Окончена: {mailing_instance.end} \n"
            )
        )
