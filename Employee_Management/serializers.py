from rest_framework import serializers
from .models import *


class LoanDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDetails
        fields = [
            'id', 'employee', 'date', 'salary_per_month',
            'loan_amount', 'previous_loan', 'total_loan',
            'balance', 'reason'
        ]

class LoanDocumentSerializer(serializers.ModelSerializer):
    # read‑only name of the employee
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = LoanDocument
        fields = [
            'id',
            'employee',
            'employee_name',
            'pdf_file',
            'uploaded_at',
        ]
        read_only_fields = ['uploaded_at']
        read_only_fields = ['uploaded_at']
        extra_kwargs = {
            'loan': {'required': False}   # don’t require loan
        }

    def validate(self, data):
        # if loan is provided, ensure it matches the employee
        loan = data.get('loan', None)
        employee = data.get('employee')
        if loan and loan.employee != employee:
            raise serializers.ValidationError(
                "If you supply a loan, it must belong to the given employee."
            )
        return data
    
class EmployeeProfileSerializer(serializers.ModelSerializer):
    loan_details = LoanDetailsSerializer(many=True, read_only=True)
    loan_documents = LoanDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Employee_profile
        fields = '__all__'
        read_only_fields = ['empid']

class SalarySerializer(serializers.ModelSerializer):
    empid = serializers.CharField(source='employee.empid', read_only=True)
    name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = Salary
        fields = '__all__'

class SalaryDocumentSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = SalaryDocument
        fields = [
            'id',
            'employee',
            'employee_name',
            'pdf_file',
            'uploaded_at',
        ]
        read_only_fields = ['uploaded_at']
