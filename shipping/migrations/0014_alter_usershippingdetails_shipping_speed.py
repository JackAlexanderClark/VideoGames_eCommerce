# Generated by Django 4.2 on 2023-06-07 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0013_alter_usershippingdetails_shipping_speed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usershippingdetails',
            name='shipping_speed',
            field=models.CharField(default='standard', max_length=50),
        ),
    ]
