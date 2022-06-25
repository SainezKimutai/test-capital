# Generated by Django 3.2 on 2022-06-22 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0020_alter_replenishment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='damagedinventory',
            name='person',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='damaged_by_base_damagedinventory_set', to=settings.AUTH_USER_MODEL, verbose_name='damaged by'),
        ),
    ]
