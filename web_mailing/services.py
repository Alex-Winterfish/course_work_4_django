from django.core.mail import send_mail
from dotenv import load_dotenv
import os
from web_mailing.models import MailingModel, MailingAttemptModel
import datetime
load_dotenv()


def start_mailing(self, form):

    from_email = os.getenv('EMAIL_HOST_USER')
    subject = form.instance.mailing.message.title
    message = form.instance.mailing.message.text
    recipients = form.instance.mailing.recipients
    mailing = MailingModel.objects.get(id=form.instance.mailing.id)
    mailing.status = "Начата"
    mailing.save()
    mailing.start = datetime.datetime.now()

    for recipient in recipients.all():
        mailing_attempt = MailingAttemptModel(mailing=form.instance.mailing)
        mailing_attempt.attempt_start = datetime.datetime.now()
        try:
            send_mail(subject, message, from_email, [recipient.email], fail_silently=False)
            mailing_attempt.status = "Успешно"
            mailing_attempt.owner = self.request.user
            mailing_attempt.save()

        except Exception as e:

            mailing_attempt.status = "Не успешно"
            mailing_attempt.server_feedback = e
            mailing_attempt.owner = self.request.user
            mailing_attempt.save()

    mailing.end = datetime.datetime.now()
    mailing.save()



