# Generated by Django 5.1.7 on 2025-03-15 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VestaRealty', '0003_monthlyrent_balance_invoices'),
    ]

    operations = [
        migrations.AddField(
            model_name='property_owned',
            name='notes',
            field=models.TextField(null=True),
        ),
    ]
