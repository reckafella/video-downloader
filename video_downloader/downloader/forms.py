from typing import Any
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from django_countries import countries

from .models import Profile

'''contains classes to handle forms'''


class DownloadURLForm(forms.Form):
    """Form to get URL from user"""
    url = forms.URLField(label='Enter URL:', max_length=100, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter URL'}))


class UserRegistrationForm(UserCreationForm):
    COUNTRIES = tuple(countries)
    username = forms.CharField(
        label='Username',
        required=True, 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})
    )
    first_name = forms.CharField(
        label='First Name',
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'})
    )
    last_name = forms.CharField(
        label='Last Name',
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'})
    )
    password1 = forms.CharField(
        label='Password', required=True, min_length=8, max_length=60,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'form3Example4cg', 'placeholder': 'Enter Password'}, render_value=True)
    )
    password2 = forms.CharField(
        label='Confirm Password', required=True, min_length=8, max_length=60,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'form3Example4cg', 'placeholder': 'Confirm Password'}, render_value=True)
    )
    dob = forms.DateField(
        label='Date of Birth',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    country = forms.ChoiceField(
        label='Country of Residence',
        required=True,
        choices=COUNTRIES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    gender = forms.ChoiceField(
        label='Gender',
        required=True,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('N', 'Prefer not to say')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    profile_pic = forms.ImageField(
        label='Profile Picture',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'formFilelg', 'type': 'file'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'dob', 'country', 'gender', 'profile_pic')

        """ labels = {
            'username': 'Username:',
            'email': 'Email Address:',
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'password1': 'Password:',
            'password2': 'Confirm Password:',
            'dob': 'Date of Birth:',
            'country': 'Country of Residence:',
            'gender': 'Gender:',
            'profile_pic': 'Profile Picture:'
        } """

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.dob=self.cleaned_data['dob']
        user.country=self.cleaned_data['country']
        user.gender=self.cleaned_data['gender']
        user.profile_pic=self.cleaned_data.get('profile_pic')

        if commit:
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    COUNTRIES = tuple(countries)
    username = forms.CharField(label='Username',
                               required=False,
                               disabled=True,
                               max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'type': 'text'}))

    bio = forms.CharField(label='Bio',
                          required=False,
                          max_length=250,
                          widget=forms.Textarea(attrs={'class': 'form-control',
                                                       'rows': 5,
                                                       'type': 'text'}))

    email = forms.EmailField(label='Email',
                             required=False,
                             disabled=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='First Name',
                             required=False,
                             max_length=30,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(label='Last Name',
                             required=False,
                             max_length=30,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    """ password1 = forms.CharField(label='Password',
                             required=False,
                             widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                               'id': 'form3Example4cg'}))

    password2 = forms.CharField(label='Confirm Password',
                             required=False,
                             widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                               'id': 'form3Example4cg'})) """

    dob = forms.DateField(label='Date of Birth',
                          required=False,
                          widget=forms.DateInput(attrs={'type': 'date',
                                                        'class': 'form-control'}))

    country = forms.ChoiceField(label='Country of Residence',
                                 required=False,
                                 choices=COUNTRIES,
                                 widget=forms.Select(attrs={'class': 'form-select'}))

    gender = forms.ChoiceField(label='Gender',
                                 required=False,
                                 choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('N', 'Prefer not to say')],
                                 widget=forms.Select(attrs={'class': 'form-select'}))

    profile_pic = forms.ImageField(label='Profile Picture',
                                   required=False,
                                   widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'formFilelg', 'type': 'file'}))

    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'dob', 'country', 'gender', 'profile_pic')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.profile.bio = self.cleaned_data['bio']
        self.user.profile.dob = self.cleaned_data['dob']
        self.user.profile.country = self.cleaned_data['country']
        self.user.profile.gender = self.cleaned_data['gender']

        if 'profile_pic' in self.changed_data and self.cleaned_data['profile_pic']:
            self.user.profile.profile_pic = self.cleaned_data['profile_pic']

        if commit:
            self.user.save()
            profile.save()

        return profile


class EmailForm(forms.Form):
    email = forms.EmailField(required=True,
                             label='Email Address:',
                             max_length=254,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control'}))


class CodeForm(forms.Form):
    code = forms.CharField(required=True,
                            label='Reset Code:',
                            min_length=6,
                            max_length=6,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}))


class NewPasswordForm(forms.Form):
    new_password =forms.CharField(label='New Password',
                                  required=True, min_length=8, max_length=60,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_new_password = forms.CharField(label='Confirm New Password',
                                           required=True, min_length=8, max_length=60,
                                           widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserPasswordChangeForm(forms.Form):
    """ The form to handle user password change """
    old_password = forms.CharField(label='Old Password',
                                   required=True, min_length=8, max_length=60,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password',
                                    required=True, min_length=8, max_length=60,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password',
                                    required=True, min_length=8, max_length=60,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("The old password is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("The two new password fields must match.")
        return cleaned_data

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user
