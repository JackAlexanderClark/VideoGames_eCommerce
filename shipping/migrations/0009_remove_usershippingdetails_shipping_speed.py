# Generated by Django 4.2 on 2023-06-07 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0008_usershippingdetails_shipping_speed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usershippingdetails',
            name='shipping_speed',
        ),
    ]