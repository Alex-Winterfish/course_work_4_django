from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime
from web_mailing.models import MessageModel, MailingModel, MailingAttemptModel, ClientModel
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "class for mailing attempts"

