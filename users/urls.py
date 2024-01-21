from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, verify_error, VerifyTemplateView, UserUpdateView, UserDetailView, UserListView, \
    change_active

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('register/verify', VerifyTemplateView.as_view(), name='verify'),
    path('register/verify_error', verify_error, name='verify_error'),
    path('profile/edit', UserUpdateView.as_view(), name='edit_profile'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('user_list', UserListView.as_view(), name='list_user'),
    path('active/<int:pk>', change_active, name='change_active'),
]
