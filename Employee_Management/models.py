from django.db import models
# from Department.models import *
from System_Admin.models import *
from django.db.models.functions import Cast
from django.db.models import IntegerField
# Create your models here.
class Employee_profile(models.Model):
    empid = models.CharField(max_length=255,primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    mobileno = models.BigIntegerField(null=True, blank=True)
    whatsapp = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(unique=True)
    adhaar = models.BigIntegerField(null=True, blank=True)
    PAN = models.CharField(max_length=255, null=True, blank=True)
    photo= models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    department = models.CharField(max_length=255,blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    monthly_salary = models.BigIntegerField(null=True, blank=True)
    date_of_joining = models.CharField(max_length=100, null=True, blank=True)
    date_of_leaving = models.CharField(max_length=100,blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    address = models.JSONField(null=True, blank=True)
    status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updates when the record changes

    # roles = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.empid:
            last_emp = (
                Employee_profile.objects
                .annotate(empid_int=Cast('empid', IntegerField()))
                .order_by('-empid_int')
                .first()
            )
            if last_emp and last_emp.empid.isdigit():
                new_id = int(last_emp.empid) + 1
            else:
                new_id = 1
            self.empid = new_id  # e.g., 0001, 0002, etc.
        super().save(*args, **kwargs)
    
