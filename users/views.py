from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.forms import PasswordResetForm

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
                registration_form.save()
                # Optionally, authenticate and login the user after registration
                username = registration_form.cleaned_data.get('username')
                password = registration_form.cleaned_data.get('password1')
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


