from django.db import models

from django import forms
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
# Create your models here.
class VideoGame(models.Model):
    video_game_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.CharField(max_length=200, default='No description provided')
    image_url = models.ImageField(upload_to='templates/videogame_imgs', default='imgs/videogames/Old_Harbour.png')

    def __str__(self):
        return self.name


