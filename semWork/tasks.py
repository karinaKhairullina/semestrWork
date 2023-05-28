from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_daily_emails():
    from subscribe.models import Subscriber
    subscribers = Subscriber.objects.filter(is_subscribed=True)
    subject = 'Ежедневное письмо'
    message = 'Привет! Это ваше ежедневное информационное письмо. Желаю вам хорошего настроения каждый день)'
    from_email = 'karihairullina@gmail.com'
    for subscriber in subscribers:
        send_mail(subject, message, from_email, [subscriber.email])
