# Generated by Django 5.2.3 on 2025-07-02 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee_Management', '0005_alter_loandetails_balance_alter_loandetails_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_period', models.CharField(blank=True, max_length=100, null=True)),
                ('present_days', models.IntegerField(blank=True, null=True)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_made', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('loan_taken', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pay', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(blank=True, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid', max_length=10, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Employee_Management.employee_profile')),
            ],
        ),
    ]
