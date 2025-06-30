from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(System_company_detail)
class SystemCompanyDetailsAdmin(admin.ModelAdmin):
     list_display = ['companyid', 'name', 'contact_person_name','alias', 'email', 'mobileno', 'whatsappno','TAX_certificate']

