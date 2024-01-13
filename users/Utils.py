from django.core.mail import EmailMessage
from django.conf import settings

class Utils():
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['subject'], body=data['body'], from_email='Support <falakshair563@gmail.com>', to=[data['to']])
        email.content_subtype = "html"
        email.send()

