from django.contrib import admin
from .models import Order,Receipt,Card,UserShippingDetails
# Register your models here.
admin.site.register(Order)
admin.site.register(Receipt)
admin.site.register(Card)
admin.site.register(UserShippingDetails)

