from django.contrib import admin
from Employee_Management.models import *
# Register your models here.

@admin.register(Employee_profile)
class EmpCompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['empid', 'name', 'mobileno', 'whatsapp', 'email',
                    'date_of_joining', 'date_of_leaving', 'department',
                    'designation','status'
                    ]

