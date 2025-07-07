from rest_framework import serializers
from django.contrib.auth import get_user_model
#from Employee_Management.models import Company_profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class EmailSerializer(serializers.Serializer):
    to = serializers.ListField(child=serializers.EmailField(), required=True)
    cc = serializers.ListField(child=serializers.EmailField(), required=False)
    subject = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    file = serializers.FileField(required=False)