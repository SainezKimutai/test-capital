# Generated by Django 3.2 on 2022-06-17 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_alter_creditnote_sales_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditnote',
            name='affects_cash',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='historicalcreditnote',
            name='affects_cash',
            field=models.BooleanField(),
        ),
    ]
