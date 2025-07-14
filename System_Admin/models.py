from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class System_company_detail(models.Model):
    companyid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_person_name = models.CharField(max_length=255, null=True, blank=True)
    # alias = models.CharField(max_length=255, blank=True, null=True)
    TAX_certificate = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    address1 = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    # whatsappno = models.CharField(max_length=15, blank=True, null=True)
    mobileno = models.CharField(max_length=15, blank=True, null=True)
    service = models.CharField(max_length=15, blank=True, null=True)
    designation = models.CharField(max_length=15, blank=True, null=True)
    brand_logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    # authorized_sign = models.ImageField(upload_to='authorized_sign/', blank=True, null=True)
    # authorized_seak = models.ImageField(upload_to='authorized_seak/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class CompanyLicense(models.Model):
    company = models.OneToOneField(System_company_detail, on_delete=models.CASCADE)
    license_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.company.name} License"