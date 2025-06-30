from rest_framework import serializers
from .models import *

class EmployeeProfileSerializer(serializers.ModelSerializer):
    department_name =  serializers.CharField(source='department.name', read_only=True)
    designation_name =  serializers.CharField(source='designation.designation', read_only=True)

    class Meta:
        model = Employee_profile
        fields = '__all__'
        read_only_fields = ['empid']  # <- Add this line

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class BankOthersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank_Others
        fields = '__all__'

class EmployeeKYCDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeKYC
        fields = '__all__'


class DocumentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_master
        fields = '__all__'
