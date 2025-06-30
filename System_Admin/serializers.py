from rest_framework import serializers
from System_Admin.models import *


class SystemCompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = System_company_detail
        fields = "__all__"

class SystemCompanyBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = System_brand_detail
        fields = "__all__"

class SystemContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = System_contact_detail
        fields = '__all__'

# class SystemSocialDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = System_social_detail
#         fields = '__all__'

# class SystemOtherDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = System_other_detail
#         fields = '__all__'




# class SystemBranchTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = System_branch_type
#         fields = '__all__'

# class SystemBranchDetailsSerializer(serializers.ModelSerializer):
#     branch_type_name = serializers.CharField(source="branch_type.type_name", read_only=True)
#     class Meta:
#         model = System_branch_details
#         fields = '__all__'

# class SystemBranchBrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = System_branch_brand
#         fields = '__all__'

# class SystemBranchContactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = System_branch_contact
#         fields = '__all__'

class SystemBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = System_bank_details
        fields = '__all__'

# class SystemBoardOfDirectorsSerializer(serializers.ModelSerializer):
#     designation_name = serializers.CharField(source="designation.designation", read_only=True)
#     class Meta:
#         model = System_Board_of_Directors
#         fields = '__all__'

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = '__all__' 






