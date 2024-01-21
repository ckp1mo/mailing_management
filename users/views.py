import random
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, ListView
from users.forms import UserRegisterForm, UserForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify')

    def form_valid(self, form):
        self.object = form.save()
        verify_code = ''.join(str(random.randrange(0, 10)) for num in range(6))
        self.object.verify_code = verify_code
        self.object.is_active = False
        self.object.save()
        send_mail(
            subject='Регистрация на портале',
            message='Поздравляем с регистрацией на портале email-рассылок Mail boom.\n'
                    f'Для завершения регистрации Вам осталось ввести код из письма: {verify_code}.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
        )
        return super().form_valid(form)


class VerifyTemplateView(TemplateView):
    template_name = 'users/verify.html'

    def post(self, request):
        verify_code = request.POST.get('verify_code')
        user = User.objects.filter(verify_code=verify_code).first()
        if user is not None and user.verify_code == verify_code:
            user.is_active = True
            user.save()
            return redirect('users:login')
        else:
            return redirect('users:verify')


def verify_error(request):
    return render(request, 'users/verify_error.html')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.block_user'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.exclude(groups=1)
        queryset = queryset.exclude(is_superuser=True)
        return queryset


def change_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = False
    user.save()
    return redirect(reverse('users:list_user'))
