from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('change_password', views.password_change, name='change_password'),
    path('download_history', views.download_history, name='download_history'),
    path('reset/', views.request_reset, name='request_reset'),
    path('reset/code/', views.enter_code, name='enter_code'),
    path('reset/<int:user_id>/<str:code>/', views.new_password, name='new_password'),
    path('youtube/', views.youtube_url_handler, name='youtube_url_handler'),
    path('youtube/download/', views.youtube_downloader, name='youtube_downloader'),
]
