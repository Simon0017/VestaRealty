# Generated by Django 5.1.7 on 2025-03-15 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VestaRealty', '0005_remove_tenant_email_tenant_id_no_tenant_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='date_joined',
            field=models.DateField(null=True),
        ),
    ]
