
from django.urls import path
from django.shortcuts import render
from gallery import urls

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery', views.gallery, name='gallery'),
    path('cart', views.cart, name='cart'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('buy', views.buy, name='buy'),
    path('register', views.register_view, name='register'),
    path('video/<int:id>',views.video,name='video'),
    path('profile', views.profile, name='profile'),

]
