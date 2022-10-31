# Generated by Django 3.2 on 2022-10-02 11:36

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_migrate_data_from_old_db'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsalesorder',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='historicalsalesorder',
            name='cash_paid',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='historicalsalesorder',
            name='mpesa_paid',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='cash_paid',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='mpesa_paid',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='historicalsalesorder',
            name='transaction_type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('CASH', 'CASH'), ('MPESA', 'MPESA'), ('CREDIT', 'CREDIT')], max_length=40),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='transaction_type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('CASH', 'CASH'), ('MPESA', 'MPESA'), ('CREDIT', 'CREDIT')], max_length=40),
        ),
    ]