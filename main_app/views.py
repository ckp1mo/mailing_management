from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from main_app.forms import MailingForm, ClientForm, MessageForm
from main_app.models import Mailing, Client, Message
from main_app.services import get_unique_client, get_random_article, mailing_count_success


def index(request):
    mailing = Mailing.objects.all()
    is_active = mailing.filter(is_active=True)
    unique_client = get_unique_client()
    random_articles = get_random_article()
    count_mailing = mailing_count_success()
    context = {
        'mailing': len(mailing),
        'is_active': len(is_active),
        'unique_client': len(unique_client),
        'articles': random_articles,
        'count_mailing': count_mailing,
    }
    return render(request, 'main_app/home.html', context)


def mailing_start():
    return call_command('mailing_start')


scheduler = BackgroundScheduler()
scheduler.add_job(mailing_start, 'interval', seconds=30)
scheduler.start()


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        if self.request.user.is_superuser or self.request.user.has_perm('users.block_user'):
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        clients = Client.objects.filter(owner=self.request.user)
        context = super().get_context_data(**kwargs)
        context['clients'] = clients
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main_app:list_view')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        form.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        clients = Client.objects.filter(owner=self.request.user.pk)
        messages = Message.objects.filter(owner=self.request.user.pk)
        context = super().get_context_data(**kwargs)
        context['clients'] = clients
        context['messages'] = messages
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user.pk)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main_app:list_view')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('main_app:list_view')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main_app:list_client')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        form.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


def check_client(request):
    client = Client.objects.all()
    if not client:
        return redirect('main_app:create_client')
    return redirect('main_app:create_view')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main_app:list_message')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        form.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user.pk)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main_app:list_message')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('main_app:list_message')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user.pk)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main_app:list_client')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main_app:list_client')


def change_active_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.is_active:
        mailing.is_active = False
    else:
        mailing.is_active = True
    mailing.save()
    return redirect(reverse_lazy('main_app:list_view'))
