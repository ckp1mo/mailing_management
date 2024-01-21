from django.contrib import admin
from main_app.models import Client, Mailing, Log, Message

admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Log)
admin.site.register(Message)