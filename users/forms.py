from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, 
        error_messages={
            'required': 'Please enter your username.',
            'max_length': 'Username should not exceed 150 characters.'
        })
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": ""}), 
        error_messages={
            'required': 'Please enter your password.'
        })

    def clean_username(self):
        username = self.cleaned_data['username']
        # Perform individual cleaning for the username field

        # Example: Ensure username is all lowercase
        cleaned_username = username.lower()

        # Example: Ensure username is at least 5 characters long
        if len(cleaned_username) < 5:
            raise forms.ValidationError('Username must be at least 5 characters long.')

        return cleaned_username
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user or not user.is_active:
                raise forms.ValidationError('Invalid username or password.')

        return cleaned_data


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'full_name', 'password1', 'password2', 'accepted_terms')

    def save(self):
        super().save()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        # Perform any additional actions here, such as logging in the user
        # or creating a session.

        # For demonstration purposes, let's print the username and password.
        print(f'Logged in with username: {username}, password: {password}')

        return 