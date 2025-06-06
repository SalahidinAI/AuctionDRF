# Generated by Django 5.2 on 2025-04-13 10:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_alter_car_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_cars', to='auction.brand'),
        ),
    ]
