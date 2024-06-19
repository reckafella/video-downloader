from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
'''contains classes to handle forms'''


class DownloadURLForm(forms.Form):
    '''Form to get URL from user'''
    url = forms.URLField(label='Enter URL:', max_length=1000, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter URL'}))


class UserRegistrationForm(UserCreationForm):
    model = User
    fields = ['username', 'email', 'password1', 'password2']
    """ labels = {
        'username': 'Username',
        'email': 'Email',
        'password1': 'Password',
        'password2': 'Confirm Password'
    } """
    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    }


class UserAuthenticationForm(AuthenticationForm):
    model = User
    fields = ['username', 'password']
    labels = {
        'username': 'Username',
        'password': 'Password'
    }
    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
        'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    }
