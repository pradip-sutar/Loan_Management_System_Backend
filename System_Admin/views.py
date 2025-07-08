from System_Admin.serializers import *
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpRequest, JsonResponse
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import timezone
from .models import *
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db import transaction
from rest_framework.response import Response
from .pagination import CustomPageNumberPagination  # Import your custom pagination class

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def company_detail_api(request):
    company_id = request.query_params.get('companyid')

    if request.method == 'GET':
        if company_id:
            try:
                company = System_company_detail.objects.get(pk=company_id)
                serializer = SystemCompanyDetailsSerializer(company)
                return JsonResponse(serializer.data)
            except System_company_detail.DoesNotExist:
                return JsonResponse({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            companies = System_company_detail.objects.all()
            serializer = SystemCompanyDetailsSerializer(companies, many=True)
            return JsonResponse(serializer.data, safe=False)
        
    elif request.method == 'POST':
        # print(request.data)
        if System_company_detail.objects.exists():
            return Response({'error': 'A company is already registered in the system. Sign In please !!'}, status=400)
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate username 
        if username and User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=400)

        serializer = SystemCompanyDetailsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # Save company
                    company = serializer.save()

                    # Create user
                    user = User.objects.create_user(username=username, password=password)
                    user.email = request.data.get('email', '')
                    user.save()

                    # Generate 7-day license
                    license_key = get_random_string(32)
                    expires_at = timezone.now() + timedelta(days=7)

                    CompanyLicense.objects.create(
                        company=company,
                        license_key=license_key,
                        expires_at=expires_at
                    )

                return Response({
                    'message': 'Company created successfully',
                    'username': username,
                    'expires_at': expires_at.strftime("%Y-%m-%d %H:%M:%S")
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': f'Something went wrong: {str(e)}'}, status=500)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not company_id:
            return JsonResponse({'error': 'companyid is required for update'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = System_company_detail.objects.get(pk=company_id)
        except System_company_detail.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SystemCompanyDetailsSerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Company updated successfully', 'data': serializer.data})
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not company_id:
            return JsonResponse({'error': 'companyid is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = System_company_detail.objects.get(pk=company_id)
            company.delete()
            return JsonResponse({'message': 'Company deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except System_company_detail.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        
        company = System_company_detail.objects.first()
        if not company:
            return JsonResponse({'error': 'Company not Register yet. Please Register to Sign In.'}, status=404)

        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        # Fetch company — assuming one company in system, or first match
        try:
            license = CompanyLicense.objects.filter(company=company).first()
            if not license:
                return JsonResponse({'error': 'License not found for this company.'}, status=403)

            if not license.is_valid():
                return JsonResponse({'error': 'License has expired.'}, status=403)

            # All OK
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
        
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})

@api_view(['POST'])
def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            profile = user.userprofile

            if profile.security_question == question and profile.security_answer == answer:
                user.set_password(new_password)
                user.save()
                return JsonResponse({'message': 'Password reset successful'})
            else:
                return JsonResponse({'error': 'Security answer mismatch'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)