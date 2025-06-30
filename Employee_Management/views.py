from django.utils.dateparse import parse_date
from .pagination import CustomPageNumberPagination  
from django.db.models import Q
from . models import *
from django.core.exceptions import ValidationError
from . serializers import *
from django.http import JsonResponse
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
# from Authentication.models import User
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import datetime, timedelta
from .models import *
# from Department.models import Department_Name
from .serializers import *

# GET and POST method for handling employee data
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def employee_profile_api(request):
    empid = request.query_params.get('empid')

    # GET Method
    if request.method == 'GET':
        if empid:
            try:
                employee = Employee_profile.objects.get(pk=empid)
                serializer = EmployeeProfileSerializer(employee)
                return Response(serializer.data)
            except Employee_profile.DoesNotExist:
                return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            employees = Employee_profile.objects.all()
            serializer = EmployeeProfileSerializer(employees, many=True)
            return Response(serializer.data)

    # POST Method
    elif request.method == 'POST':
        serializer = EmployeeProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT Method
    elif request.method == 'PUT':
        if not empid:
            return Response({'error': 'empid is required for update'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = Employee_profile.objects.get(pk=empid)
        except Employee_profile.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeProfileSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee updated successfully', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE Method
    elif request.method == 'DELETE':
        if not empid:
            return Response({'error': 'empid is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = Employee_profile.objects.get(pk=empid)
            employee.delete()
            return Response({'message': 'Employee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Employee_profile.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
