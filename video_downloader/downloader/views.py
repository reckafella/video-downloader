from django.shortcuts import render, redirect
from django.http import HttpResponse
from pytube import YouTube
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import io
from .forms import DownloadURLForm, UserRegistrationForm, UserAuthenticationForm


"""
This view is for rendering the home page
"""
def home(request):
    '''View to render home page'''
    return render(request, 'downloader/home.html')


"""
The following views are for handling user authentication
"""
def signup_view(request):
    '''View to handle user registration'''
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    '''View to handle user login'''
    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    '''View to handle user logout'''
    logout(request)
    return redirect('home')


def csrf_failure(request, reason=""):
    '''View to handle CSRF failures'''
    return render(request, 'errors/csrf_failure.html', {
        'reason': reason,
    })


""" 
The following views are for handling YouTube video/audio downloads
"""

@login_required
def youtube_url_handler(request):
    '''View to handle form submission for YouTube URL'''
    if request.method == 'POST':
        form = DownloadURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            yt = YouTube(url)
            request.session['video_url'] = url

            # get all available video and audio streams
            video_streams = yt.streams.filter(progressive=True)
            audio_streams = yt.streams.filter(only_audio=True)

            choices = [(stream.itag, f'{stream.mime_type} {stream.resolution or stream.abr}') for stream in video_streams] + \
                      [(stream.itag, f'{stream.mime_type} {stream.abr}') for stream in audio_streams]

            request.session['choices'] = choices
            request.session['title'] = yt.title
            request.session['thumbnail_url'] = yt.thumbnail_url

            return redirect('youtube_downloader')
    else:
        form = DownloadURLForm()

    return render(request, 'downloader/yt_index.html', {'form': form})

@login_required
def youtube_downloader(request):
    '''View to render page with download options'''
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

    return render(request, 'downloader/yt_download.html', context)
