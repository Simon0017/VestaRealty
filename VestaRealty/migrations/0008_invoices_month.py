# Generated by Django 5.1.7 on 2025-03-18 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VestaRealty', '0007_alter_invoices_balance_carried_down'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='month',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
