# Generated by Django 3.2 on 2022-06-04 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_auto_20220529_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalreplenishment',
            name='delivery_number',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='replenishment',
            name='delivery_number',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
