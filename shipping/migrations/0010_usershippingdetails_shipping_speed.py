# Generated by Django 4.2 on 2023-06-07 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0009_remove_usershippingdetails_shipping_speed'),
    ]

    operations = [
        migrations.AddField(
            model_name='usershippingdetails',
            name='shipping_speed',
            field=models.CharField(default='standard', max_length=50),
            preserve_default=False,
        ),
    ]
