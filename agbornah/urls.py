from django.contrib import admin
from django.urls import path
from users.views import AuthView, ForgetPasswordView, UsersView, users_list
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", AuthView.as_view(), name="auth-listview"),
    path('forget_password/', ForgetPasswordView.as_view(), name='forget_password'),

    # Password reset URLs
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path("users/", users_list, name="users-list"),

    path("home/", login_required(TemplateView.as_view(template_name="home.html"))),
    path('admin/', admin.site.urls),
]
