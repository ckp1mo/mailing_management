from django.core.management import BaseCommand
from main_app.models import Mailing, Log, Message
from main_app.services import send_mail_to_client, check_mailing_time


class Command(BaseCommand):
    def handle(self, *args, **options):
        check_mailing_time()
        mailing = Mailing.objects.filter(is_active=True)
        for mail in mailing:
            if mail.status == 'Запущена':
                clients = mail.clients.all()
                message = Message.objects.get(pk=mail.message_id)
                if clients is None:
                    log = Log.objects.create(
                        status='Failed',
                        server_response='Отсутствуют клиенты',
                        owner=mail.owner,
                        mailing=message,
                    )
                    log.save()
                    continue
                else:
                    for client in clients:
                        try:
                            send_mail_to_client(message, client)
                        except ConnectionRefusedError as error:
                            log = Log.objects.create(
                                status='Failed',
                                server_response=error,
                                owner=mail.owner,
                                mailing=message,
                                client=client.email,
                            )
                            log.save()
                        else:
                            log = Log.objects.create(
                                status='Success',
                                server_response='',
                                owner=mail.owner,
                                mailing=mail,
                                client=client.email,
                            )
                            log.save()
                            mail.status = 'Создана'
                            mail.save()
