# Generated by Django 3.2 on 2022-06-22 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20220622_2223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='damagedinventory',
            options={'ordering': ['-modified', '-created']},
        ),
        migrations.AlterModelOptions(
            name='inventory',
            options={'ordering': ['-modified', '-created']},
        ),
        migrations.AlterModelOptions(
            name='promotion',
            options={'ordering': ['-modified', '-created']},
        ),
    ]