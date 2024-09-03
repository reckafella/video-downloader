from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from pytube import YouTube
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import io

from .forms import DownloadURLForm, UserPasswordChangeForm
from .forms import EmailForm, CodeForm, NewPasswordForm, ProfileUpdateForm, UserRegistrationForm
from .models import PasswordResetCode
from .passwords import PasswordReset

"""
This view is for rendering the home page
"""


def home(request):
    """View to render home page"""
    return render(request, 'downloader/home.html')


"""
The following views are for handling user authentication
"""


def signup_view(request):
    """View to handle user registration"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
            else:
                user = form.save(commit=False)
                user.email = email
                user.save()
                login(request, user)
                messages.success(request, 'Account created successfully')
                return redirect('home')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'page_title': 'Create Account',
        'form_title': 'Create Account',
        'submit_text': 'Signup',
        'extra_messages': [{'text': 'Already have an account? ', 'url': reverse_lazy('login'), 'link_text': 'Login'}]
    }
    return render(request, 'registration/signup.html', context)



def login_view(request):
    """View to handle user login"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise User.DoesNotExist
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Hi {user.username}, Welcome!')
                return redirect('home')
            else:
                messages.error(request, 'Disabled account!')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        pass

    return render(request, 'registration/login.html')


def logout_view(request):
    """View to handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')


def request_reset(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                code = PasswordReset.generate_code()
                PasswordResetCode.objects.create(user=user, code=code)
                PasswordReset.send_email(email, code)
                messages.success(request, 'A reset code has been sent to your email')
                return redirect('enter_code')
            except User.DoesNotExist:
                messages.error(request, 'No user found with that email address.')
    else:
        form = EmailForm()
    context = {
        'form': form,
        'page_title': 'Reset your Password',
        'form_title': 'Request Passcode',
        'submit_text': 'Request Passcode',
        'extra_messages': [
            {'text': "Don't have an account? ", 'url': reverse_lazy('login'), 'link_text': 'Login'}]
    }
    return render(request, 'registration/reset-password.html', context)


def enter_code(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                reset_code = PasswordResetCode.objects.get(code=code)
                return redirect('new_password', user_id=reset_code.user.id, code=code)
            except PasswordResetCode.DoesNotExist:
                messages.error(request, 'Invalid code.')
    else:
        form = CodeForm()

    context = {
        'form': form,
        'page_title': 'Reset your Password',
        'form_title': 'Enter Passcode',
        'submit_text': 'Submit',
        'extra_messages': [
            {'text': "Don't have an account? ", 'url': reverse_lazy('login'), 'link_text': 'Login'}]
    }
    return render(request, 'registration/reset-password.html', context)


def new_password(request, user_id, code):
    try:
        user = User.objects.get(id=user_id)
        reset_code = PasswordResetCode.objects.get(user=user, code=code)
    except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
        messages.error(request, 'Invalid reset attempt.')
        return redirect('request_reset')

    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('new_password')
            password2 = form.cleaned_data.get('confirm_new_password')
            if password1 == password2:
                user.set_password(password1)
                user.save()
                reset_code.delete()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
            else:
                messages.error(request, 'An error occurred! Check passwords match and try again.')
    else:
        form = NewPasswordForm()

    context = {
        'form': form,
        'page_title': 'Reset your Password',
        'form_title': 'Set New Password',
        'submit_text': 'Set New Password',
        'extra_messages': [
            {'text': "Don't have an account? ", 'url': reverse_lazy('login'), 'link_text': 'Login'}]
    }
    return render(request, 'registration/reset-password.html', context)


@login_required
def view_profile(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('view_profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile, user=request.user)
    
    context = {
        'form': form,
        'page_title': 'Edit your Profile',
        'form_title': 'Edit Profile',
        'submit_text': 'Save Changes',
        'extra_messages': [
            {'text': "Go back to your ", 'url': reverse_lazy('view_profile'), 'link_text': 'Profile'}]
    }
    return render(request, 'accounts/edit-profile.html', context)


@login_required
def password_change(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated! Redirecting to Home.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserPasswordChangeForm(request.user)

    context = {
        'form': form,
        'page_title': 'Change Password',
        'form_title': 'Change Password',
        'submit_text': 'Save Changes',
        'extra_messages': [{'text': 'Cancel Process? ', 'url': reverse('home'), 'link_text': 'Home'}]
    }
    return render(request, 'registration/reset-password.html', context)


def csrf_failure(request, reason=""):
    """View to handle CSRF failures"""
    return render(request, 'errors/csrf-failure.html', {
        'reason': reason,
    })


""" 
The following views are for handling YouTube video/audio downloads
"""


@login_required
def youtube_url_handler(request):
    """View to handle form submission for YouTube URL"""
    if request.method == 'POST':
        form = DownloadURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            yt = YouTube(url)
            request.session['video_url'] = url

            # get all available video and audio streams
            video_streams = yt.streams.filter(progressive=True)
            audio_streams = yt.streams.filter(only_audio=True)

            choices = [(stream.itag, f'{stream.mime_type} {stream.resolution or stream.abr}') for stream in
                       video_streams] + \
                      [(stream.itag, f'{stream.mime_type} {stream.abr}') for stream in audio_streams]

            request.session['choices'] = choices
            request.session['title'] = yt.title
            request.session['thumbnail_url'] = yt.thumbnail_url

            return redirect('youtube_downloader')
    else:
        form = DownloadURLForm()

    return render(request, 'downloader/yt-index.html', {'form': form})


@login_required
def youtube_downloader(request):
    """View to render page with download options"""
    if 'choices' not in request.session:
        return redirect('youtube_url_handler')

    if request.method == 'POST':
        itag = request.POST.get('itag')
        if itag:
            url = request.session['video_url']
            yt = YouTube(url)
            stream = yt.streams.get_by_itag(itag)

            # Create a stream buffer
            buffer = io.BytesIO()
            stream.stream_to_buffer(buffer)
            buffer.seek(0)

            # Prepare the response
            response = HttpResponse(buffer, content_type=stream.mime_type)
            response['Content-Disposition'] = f'attachment; filename="{yt.title}.{stream.subtype}"'
            return response

    # Prepare data for rendering
    choices = request.session['choices']
    thumbnail_url = request.session['thumbnail_url']
    title = request.session['title']

    context = {
        'choices': choices,
        'thumbnail_url': thumbnail_url,
        'title': title,
    }

    return render(request, 'downloader/yt-dl.html', context)


def contact(request):
    """ View to render contact page """
    return render(request, 'downloader/contact.html')


def about(request):
    """ View to render the about page """
    return render(request=request, template_name='downloader/about.html')


def download_history(request):
    """ View to display all download requests for each user """

    # Get all download requests for the current user
    download_requests = {'first': 'link',
                         'second': 'link',
                         'third': 'link',
                         'fourth': 'link'
                         }

    context = {
        'download_requests': download_requests,
    }

    return render(request, 'downloader/download-history.html', context)
