# Generated by Django 3.2 on 2022-05-22 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_auto_20220519_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinventory',
            name='recent_buying_price',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='recent_buying_price',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
