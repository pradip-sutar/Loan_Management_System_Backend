# Generated by Django 5.2.3 on 2025-07-02 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee_Management', '0007_loandetails_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_profile',
            name='total_loan_amount',
            field=models.BigIntegerField(default=0),
        ),
    ]
