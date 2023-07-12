from django.urls import path
from . import views

urlpatterns = [
    path('buy', views.buy, name='buy'),
    path('cart', views.cart, name='cart'),
    path('receipt', views.receipt, name='receipt'),
]