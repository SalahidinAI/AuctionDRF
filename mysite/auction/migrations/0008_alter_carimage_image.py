# Generated by Django 5.2 on 2025-04-13 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0007_remove_car_car_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carimage',
            name='image',
            field=models.ImageField(upload_to='car_images/'),
        ),
    ]
