# Generated by Django 3.2 on 2022-06-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_auto_20220604_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='damagedinventory',
            name='replaced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicaldamagedinventory',
            name='replaced',
            field=models.BooleanField(default=False),
        ),
    ]
