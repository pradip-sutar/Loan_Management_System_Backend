# Generated by Django 5.2.3 on 2025-07-01 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System_Admin', '0004_remove_system_company_detail_tax_certificate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='system_company_detail',
            name='TAX_certificate',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
