import time
from django.core.mail import send_mail
from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest

@shared_task
def send_email_task(user_id):
    from authorization.models import User
    user = User.objects.get(pk=user_id)
    subject = 'Сброс пароля'
    request = HttpRequest()
    request.META['SERVER_NAME'] = 'localhost'
    request.META['SERVER_PORT'] = '8000'
    reset_url = generate_reset_url(user_id, request)
    message = f'Здравствуйте,\n\nВы получили это письмо, потому что запросили сброс пароля для вашей учетной записи.\n\nПожалуйста, перейдите по следующей ссылке, чтобы сбросить пароль:\n{reset_url}\n\nЕсли вы не запрашивали сброс пароля, просто проигнорируйте это сообщение.'
    from_email = 'karihairullina@gmail.com'
    recipient_list = [user.email]
    time.sleep(5)
    send_mail(subject, message, from_email, recipient_list)


def generate_reset_url(user_id, request):
    current_site = get_current_site(request)
    domain = current_site.domain
    reset_url = f'http://{domain}/reset-password/{user_id}/'
    return reset_url
