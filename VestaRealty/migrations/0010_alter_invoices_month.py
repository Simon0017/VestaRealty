# Generated by Django 5.1.7 on 2025-03-21 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VestaRealty', '0009_paid_invoices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='month',
            field=models.CharField(max_length=20),
        ),
    ]
