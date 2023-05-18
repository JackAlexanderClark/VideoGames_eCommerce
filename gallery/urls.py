
from django.urls import path
from django.shortcuts import render
from gallery import urls

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home),
    path('gallery', views.gallery, name='gallery'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
]
