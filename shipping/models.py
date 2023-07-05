from django.db import models
from django.contrib.auth.models import User
from gallery.models import VideoGame

class UserShippingDetails(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line = models.CharField(max_length=512)
    postcode = models.CharField(max_length=10)
    phone_number = models.BigIntegerField()
    country = models.CharField(max_length=50)
    speed=models.CharField(max_length=100, default="standard")


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id= models.ForeignKey(VideoGame,on_delete=models.CASCADE)
    quantity= models.IntegerField(default=1)
    is_processed = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_option = models.CharField(max_length=50)
    delivery_cost = models.IntegerField()

    def __str__(self):
        return self.user_id.username+" "+self.game_id.name

class Card(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.BigIntegerField()
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    cvc=models.IntegerField()


class Receipt(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount=models.IntegerField()
    receipt_id=models.AutoField(primary_key=True)
    items = models.TextField()
    tax=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    delivery_option=models.CharField(max_length=100)






