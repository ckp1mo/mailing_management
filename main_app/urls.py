from django.urls import path

from main_app.apps import MainAppConfig
from main_app.views import index, MailingListView, MailingCreateView, MailingUpdateView, MailingDetailView, \
    MailingDeleteView, ClientCreateView, check_client, MessageCreateView, ClientListView, MessageListView, \
    ClientUpdateView, ClientDeleteView, ClientDetailView, MessageUpdateView, MessageDetailView, MessageDeleteView, \
    change_active_mailing

app_name = MainAppConfig.name


urlpatterns = [
    path('', index, name='index'),
    path('check_client', check_client, name='check_client'),
    path('list', MailingListView.as_view(), name='list_view'),
    path('create', MailingCreateView.as_view(), name='create_view'),
    path('edit/<int:pk>', MailingUpdateView.as_view(), name='update_view'),
    path('detail/<int:pk>', MailingDetailView.as_view(), name='detail_view'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='delete_view'),
    path('change_active/<int:pk>', change_active_mailing, name='change_active'),
    path('client', ClientListView.as_view(), name='list_client'),
    path('create_client', ClientCreateView.as_view(), name='create_client'),
    path('edit_client/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('detail_client/<int:pk>', ClientDetailView.as_view(), name='detail_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    path('message', MessageListView.as_view(), name='list_message'),
    path('create_message', MessageCreateView.as_view(), name='create_message'),
    path('edit_message/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('detail_message/<int:pk>', MessageDetailView.as_view(), name='detail_message'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
]
