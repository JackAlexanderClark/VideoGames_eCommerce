from django.db import models

# Create your models here.
class VideoGame(models.Model):
    video_game_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512)
    genre = models.CharField(max_length=512)
    price = models.IntegerField()
    quantity = models.IntegerField()
    #description = models.CharField(max_length=512)
    image_url = models.ImageField(upload_to='templates/videogame_imgs', default='imgs/videogames/Old_Harbour.png')

    def __str__(self):
        return self.name


