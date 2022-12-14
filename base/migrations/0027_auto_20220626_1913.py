# Generated by Django 3.2 on 2022-06-26 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_merge_0023_auto_20220622_2314_0025_auto_20220617_1635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='creditnote',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='finish',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='range',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='replenishmentitem',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='salesitem',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='salesorder',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-created', '-modified']},
        ),
        migrations.AddField(
            model_name='historicalinventory',
            name='max_selling_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inventory',
            name='max_selling_price',
            field=models.IntegerField(default=0),
        ),
    ]
