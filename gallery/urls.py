
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
    path('receipt', views.receipt, name='receipt'),
    path('remove_game_item/<str:id>', views.remove_game_item, name='remove_game_item'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('load_edit_profile', views.load_edit_profile, name='load_edit_profile'),
    path('add_game_item/<str:id>', views.add_game_item, name='add_game_item'),
    path('delete_game_item/<str:id>', views.delete_game_item, name='delete_game_item'),
]
