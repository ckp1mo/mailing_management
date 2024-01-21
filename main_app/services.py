import datetime
import random
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from blog.models import Blog
from main_app.models import Mailing, Log, Client


def send_mail_to_client(message, client):
    send_mail(
        subject=message.title,
        message=message.body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[client.email],
    )


def check_mailing_time():
    mail_time = Mailing.objects.filter(is_active=True)
    time_now = datetime.datetime.now(datetime.timezone.utc)
    for mail in mail_time:
        time_log = Log.objects.filter(mailing=mail.pk).order_by('-time').first()
        if mail.start_time < datetime.datetime.now().time() < mail.end_time:
            if time_log is None:
                mail.status = 'Запущена'
                mail.save()
                continue
            # time_delta - это разница между текущим временем и временем последней рассылки в секундах
            time_delta = (time_now - time_log.time).seconds / 60 / 60 / 24  # значением этого выражением будет колличество дней
            if mail.frequency == 'Раз в день':
                if time_delta >= 1:
                    mail.status = 'Запущена'
                    mail.save()
            elif mail.frequency == 'Раз в неделю':
                if time_delta >= 7:
                    mail.status = 'Запущена'
                    mail.save()
            elif mail.frequency == 'Раз в месяц':
                if time_delta >= 30:
                    mail.status = 'Запущена'
                    mail.save()


def get_unique_client():
    clients = Client.objects.all()
    client_email = []
    if clients is None:
        return None
    else:
        for client in clients:
            client_email.append(client.email)
    unique_client = set(client_email)
    return unique_client


def get_random_article():
    articles = Blog.objects.all()
    blog_list = []
    if articles is None:
        return None
    else:
        for article in articles:
            blog_list.append(article)
        random.shuffle(blog_list)
        return blog_list[:3]


def mailing_count_success():
    mailing = cache_mailing_count_success()
    if mailing is None:
        return None
    else:
        return len(mailing.filter(status='Success'))


def cache_mailing_count_success():
    if settings.CACHE_ENABLED:
        key = 'mailing_count'
        mailing_count = cache.get(key)
        if mailing_count is None:
            mailing_count = Log.objects.all()
            cache.set(key, mailing_count)
    else:
        mailing_count = Log.objects.all()
    return mailing_count
