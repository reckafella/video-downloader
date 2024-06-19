from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile', views.home, name='home'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('youtube', views.youtube_url_handler, name='youtube_url_handler'),
    path('youtube/download', views.youtube_downloader, name='youtube_downloader'),
]
