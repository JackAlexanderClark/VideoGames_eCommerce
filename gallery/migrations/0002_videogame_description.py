# Generated by Django 4.2 on 2023-07-05 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videogame',
            name='description',
            field=models.CharField(default='No description provided', max_length=512),
        ),
    ]
