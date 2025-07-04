# Generated by Django 5.2.1 on 2025-05-13 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='System_company_detail',
            fields=[
                ('companyid', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('alias', models.CharField(blank=True, max_length=255, null=True)),
                ('company_size', models.CharField(blank=True, max_length=255, null=True)),
                ('incorporation_no', models.CharField(blank=True, max_length=255, null=True)),
                ('incorporation_certificate', models.FileField(blank=True, null=True, upload_to='incorporation_certificate/')),
                ('incorporation_date', models.CharField(blank=True, max_length=100, null=True)),
                ('PAN', models.CharField(blank=True, max_length=255, null=True)),
                ('TAX_certificate', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('pincode', models.CharField(blank=True, max_length=20, null=True)),
                ('registered_office_details', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('whatsappno', models.CharField(blank=True, max_length=15, null=True)),
                ('mobileno', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='System_brand_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_logo', models.ImageField(blank=True, null=True, upload_to='brand_logos/')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='favicons/')),
                ('letter_header', models.ImageField(blank=True, null=True, upload_to='letter_headers/')),
                ('letter_footer', models.ImageField(blank=True, null=True, upload_to='letter_footers/')),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='System_Admin.system_company_detail')),
            ],
        ),
        migrations.CreateModel(
            name='System_contact_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('designation', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobileno', models.CharField(blank=True, max_length=15, null=True)),
                ('whatsapp', models.CharField(blank=True, max_length=15, null=True)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='System_Admin.system_company_detail')),
            ],
        ),
    ]
