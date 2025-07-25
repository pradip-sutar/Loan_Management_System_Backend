# Generated by Django 5.2.3 on 2025-07-01 12:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee_Management', '0003_employee_profile_remove_address_employee_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('salary_per_month', models.BigIntegerField()),
                ('loan_amount', models.BigIntegerField()),
                ('previous_loan', models.BigIntegerField(default=0)),
                ('total_loan', models.BigIntegerField()),
                ('balance', models.BigIntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan_details', to='Employee_Management.employee_profile')),
            ],
        ),
    ]
