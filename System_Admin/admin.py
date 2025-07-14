from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(System_company_detail)
class SystemCompanyDetailsAdmin(admin.ModelAdmin):
     list_display = ['companyid', 'name', 'contact_person_name','TAX_certificate','email', 'mobileno']


@admin.register(CompanyLicense)
class CompanyLicenseAdmin(admin.ModelAdmin):
    list_display = ['company', 'license_key', 'created_at', 'expires_at', 'is_valid']
    search_fields = ['company__name', 'license_key']
    list_filter = ['expires_at']
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Valid'

