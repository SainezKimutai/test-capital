# Generated by Django 3.2 on 2022-06-17 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20220607_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditnote',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalcreditnote',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
