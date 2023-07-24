from django.views import View
from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.forms import PasswordResetForm
from .signals import user_registered as user_registered_signal
from django.db import transaction as tx
from django.http import Http404
from django.core.paginator import Paginator

def users_list(request):
    user_list = User.objects.all()
    paginator = Paginator(user_list, 2)  # Show 2 user per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "users/list.html", {"page_obj": page_obj})

class UsersView(ListView):
    model = User
    paginate_by = 2
    template_name = "users/list.html"


class ForgetPasswordView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'users/forget_password.html', {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                from_email=None,
                email_template_name='users/password_reset_email.html',
                subject_template_name='users/password_reset_subject.txt',
            )
            return render(request, 'users/password_reset_done.html')
        return render(request, 'users/forget_password.html', {'form': form})
    

class AuthView(View):

    def get(self, request, *args, **kwargs):
        registration_form = RegistrationForm()
        login_form = LoginForm()
        return render(request, 'users/auth.html', {'registration_form': registration_form, 'login_form': login_form})

    def post(self, request, *args, **kwargs):
        registration_form = RegistrationForm()
        login_form = LoginForm()
        if 'register' in request.POST:
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                # Optionally, authenticate and login the user after registration
                username = registration_form.cleaned_data.get('username')
                password = registration_form.cleaned_data.get('password1')
                user_register(username=username, password=password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/home')
        elif 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                print("post loginrequest")
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/home')
                else:
                    login_form.add_error(None, 'Invalid username or password.')

        return render(request, 'users/auth.html', {'registration_form': registration_form, 'login_form': login_form})

def is_user_already_registered(*, username:str):
    if User.objects.filter(username__iexact=username).exists():
        return (True, _("Username is already in use."))

    return (False, None)

@tx.atomic
def user_register(username:str, password:str):
    is_registered, reason = is_user_already_registered(username=username)
    if is_registered:
        raise Http404(reason)

    user = User(username=username)
    user.set_password(password)
    try:
        user.save()
    except:
        raise Http404(_("User is already registered."))

    user_registered_signal.send(sender=user.__class__, user=user)
    return user
