import re
from django.db import models
from System_Admin.models import *
from django.db.models.functions import Cast
from django.db.models import IntegerField, Max
# Create your models here.
class Employee_profile(models.Model):
    empid = models.CharField(max_length=255,primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    mobileno = models.BigIntegerField(null=True, blank=True)
    whatsapp = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
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
    total_loan_amount = models.BigIntegerField(default=0)

    # roles = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.empid:
            last_emp = Employee_profile.objects.aggregate(max_id=Max('empid'))
            last_id = last_emp.get('max_id')

            if last_id and re.match(r'^EMP\d{3}$', last_id):
                last_num = int(last_id[3:])
                new_id = f'EMP{last_num + 1:03d}'
            else:
                new_id = 'EMP001'

            self.empid = new_id
        super().save(*args, **kwargs)
    
class LoanDetails(models.Model):
    employee = models.ForeignKey(Employee_profile, on_delete=models.CASCADE, related_name='loan_details')
    date = models.DateField(null=True, blank=True)
    salary_per_month = models.BigIntegerField(null=True, blank=True)
    loan_amount = models.BigIntegerField(null=True, blank=True)
    previous_loan = models.BigIntegerField(default=0)
    total_loan = models.BigIntegerField(null=True, blank=True, default=0)
    balance = models.BigIntegerField(null=True, blank=True)
    updated_bal = models.BigIntegerField(null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if self.employee:
    #         self.balance = self.employee.monthly_salary - self.employee.total_loan_amount
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan for {self.employee.empid} on {self.date}"
    
class LoanDocument(models.Model):
    employee = models.ForeignKey(Employee_profile, on_delete=models.CASCADE, related_name='loan_documents')
    pdf_file = models.FileField(upload_to='loan_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.employee.name}"
    
class Salary(models.Model):
    STATUS_CHOICES = (
        ('paid', 'PAID'),
        ('partial', 'PARTIAL'),
        ('unpaid', 'UNPAID'),
    )

    pay_period = models.CharField(max_length=100, null=True, blank=True)
    employee = models.ForeignKey(Employee_profile, on_delete=models.CASCADE, null=True, blank=True)
    present_days = models.IntegerField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_made = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    loan_taken = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.empid if self.employee else 'Unknown'} - {self.pay_period}"
    
class SalaryDocument(models.Model):
    employee = models.ForeignKey(Employee_profile, on_delete=models.CASCADE, related_name='salary_documents')
    pdf_file = models.FileField(upload_to='salary_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Salary Document for {self.employee.name}"