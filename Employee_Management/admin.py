from django.contrib import admin
from Employee_Management.models import *
# Register your models here.

@admin.register(Employee_profile)
class EmpCompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['empid', 'name', 'mobileno', 'whatsapp', 'email',
                    'date_of_joining', 'date_of_leaving', 'department',
                    'designation','status', 'total_loan_amount'
                    ]


@admin.register(LoanDetails)
class LoanDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','employee', 'employee_name', 'date', 'loan_amount', 'balance', 'reason')
    search_fields = ('employee__empid', 'employee__name')
    list_filter = ('date',)

    def employee_name(self, obj):
        return obj.employee.name
    employee_name.short_description = 'Employee Name'

@admin.register(LoanDocument)
class LoanDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('employee__name', 'loan__reason')

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('pay_period', 'employee', 'present_days', 'salary', 'salary_made', 'loan_taken', 'balance', 'pay', 'status')
    search_fields = ('employee__empid', 'employee__name', 'pay_period')

@admin.register(SalaryDocument)
class SalaryDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('employee__name',)