from System_Admin.serializers import *
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
# from Department.models import *
# from Employee_Management.models import *
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db import transaction, IntegrityError
import re
import random
from rest_framework import status
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
            return JsonResponse(serializer.data)

    elif request.method == 'POST':
        serializer = SystemCompanyDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Company created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
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
        
