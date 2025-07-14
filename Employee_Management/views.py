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
# import pandas as pd
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.views import APIView

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def employee_profile_api(request):
    empid = request.query_params.get('empid')

    # ✅ GET Method
    if request.method == 'GET':
        if empid:
            try:
                employee = Employee_profile.objects.get(pk=empid)
                serializer = EmployeeProfileSerializer(employee)
                data = serializer.data

                data.pop('total_loan_amount', None)

                total_loan_sum = 0
                for loan in data.get('loan_details', []):
                    loan_amount = loan.get('loan_amount') or 0
                    previous_loan = loan.get('previous_loan') or 0
                    total_loan = loan_amount + previous_loan
                    loan['total_loan'] = total_loan
                    total_loan_sum += total_loan

                data['total_loan_amount'] = total_loan_sum


                salaries = Salary.objects.filter(employee=employee)
                salary_serializer = SalarySerializer(salaries, many=True)
                salary_data = salary_serializer.data

                for sal in salary_data:
                    pay = float(sal.get('pay') or 0)
                    balance = float(sal.get('balance') or 0)
                    if pay == 0:
                        sal['status'] = 'PENDING'
                    elif balance == 0:
                        sal['status'] = 'PAID'
                    else:
                        sal['status'] = 'PARTIAL'

                data['salary_details'] = salary_data

                salary_docs = SalaryDocument.objects.filter(employee=employee)
                salary_doc_serializer = SalaryDocumentSerializer(salary_docs, many=True)
                data['salary_documents'] = salary_doc_serializer.data

                return Response(data)

            except Employee_profile.DoesNotExist:
                return Response({'error': 'Employee not found'}, status=404)

        else:
            employees = Employee_profile.objects.all().order_by('-empid')

            # 📌 Apply filters
            name = request.query_params.get('name')
            department = request.query_params.get('department')
            designation = request.query_params.get('designation')
            status_param = request.query_params.get('status')
            joining_from = request.query_params.get('joining_from')
            joining_to = request.query_params.get('joining_to')
            leaving_from = request.query_params.get('leaving_from')
            leaving_to = request.query_params.get('leaving_to')

            if name:
                employees = employees.filter(name__icontains=name)
            if department:
                employees = employees.filter(department__icontains=department)
            if designation:
                employees = employees.filter(designation__icontains=designation)
            if status_param:
                if status_param.lower() == 'true':
                    employees = employees.filter(status=True)
                elif status_param.lower() == 'false':
                    employees = employees.filter(status=False)

            if joining_from:
                employees = employees.filter(date_of_joining__gte=joining_from)
            if joining_to:
                employees = employees.filter(date_of_joining__lte=joining_to)

            # ✅ Apply date_of_leaving range filters
            if leaving_from:
                employees = employees.filter(date_of_leaving__gte=leaving_from)
            if leaving_to:
                employees = employees.filter(date_of_leaving__lte=leaving_to)

            paginator = CustomPageNumberPagination()
            result_page = paginator.paginate_queryset(employees, request)
            serializer = EmployeeProfileSerializer(result_page, many=True)
            data_list = serializer.data

            for data in data_list:
                data.pop('total_loan_amount', None)

                total_loan_sum = 0
                for loan in data.get('loan_details', []):
                    loan_amount = loan.get('loan_amount') or 0
                    previous_loan = loan.get('previous_loan') or 0
                    total_loan = loan_amount + previous_loan
                    loan['total_loan'] = total_loan
                    total_loan_sum += total_loan

                data['total_loan_amount'] = total_loan_sum

                try:
                    employee = Employee_profile.objects.get(empid=data['empid'])
                except Employee_profile.DoesNotExist:
                    employee = None

                if employee:
                    salaries = Salary.objects.filter(employee=employee)
                    salary_serializer = SalarySerializer(salaries, many=True)
                    salary_data = salary_serializer.data


                    for sal in salary_data:
                        pay = float(sal.get('pay') or 0)
                        balance = float(sal.get('balance') or 0)
                        if pay == 0:
                            sal['status'] = 'PENDING'
                        elif balance == 0:
                            sal['status'] = 'PAID'
                        else:
                            sal['status'] = 'PARTIAL'

                    data['salary_details'] = salary_data

                    salary_docs = SalaryDocument.objects.filter(employee=employee)
                    salary_doc_serializer = SalaryDocumentSerializer(salary_docs, many=True)
                    data['salary_documents'] = salary_doc_serializer.data
                else:
                    data['salary_details'] = []
                    data['salary_documents'] = []

            return paginator.get_paginated_response(data_list)
        
    elif request.method == 'POST':
        serializer = EmployeeProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee created successfully', 'data': serializer.data}, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'PUT':
        if not empid:
            return Response({'error': 'empid is required for update'}, status=400)
        try:
            employee = Employee_profile.objects.get(pk=empid)
        except Employee_profile.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)

        serializer = EmployeeProfileSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee updated successfully', 'data': serializer.data})
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not empid:
            return Response({'error': 'empid is required for deletion'}, status=400)
        try:
            employee = Employee_profile.objects.get(pk=empid)
            employee.delete()
            return Response({'message': 'Employee deleted successfully'}, status=204)
        except Employee_profile.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def loan_details_api(request):
    loan_id = request.query_params.get('id')

    # === GET Single Loan Record ===
    if request.method == 'GET':
        if loan_id:
            try:
                loan = LoanDetails.objects.get(pk=loan_id)
            except LoanDetails.DoesNotExist:
                return Response({'error': 'Loan not found'}, status=404)

            employee = loan.employee
            serializer = LoanDetailsSerializer(loan)
            response = serializer.data

            response['employeename'] = employee.name
            response['total_loan'] = (loan.loan_amount or 0) + (loan.previous_loan or 0)
            response['employee_details'] = {
                'name': employee.name,
                'designation': employee.designation,
                'department': employee.department,
                'mobileno': employee.mobileno,
                'adhaar': employee.adhaar,
                'PAN': employee.PAN
            }

            documents = LoanDocument.objects.filter(employee=employee)
            response['loan_documents'] = [
                {
                    'id': doc.id,
                    'pdf_file': request.build_absolute_uri(doc.pdf_file.url),
                    'uploaded_at': doc.uploaded_at
                }
                for doc in documents
            ]

            return Response(response)

        # === GET All Loans (with Filters & Pagination) ===
        loans = LoanDetails.objects.select_related('employee').all().order_by('-date')

        # 📌 Filters
        employee_name = request.query_params.get('employee_name')
        department = request.query_params.get('department')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        if employee_name:
            loans = loans.filter(employee__name__icontains=employee_name)
        if department:
            loans = loans.filter(employee__department__icontains=department)
        if from_date:
            loans = loans.filter(date__gte=from_date)
        if to_date:
            loans = loans.filter(date__lte=to_date)

        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(loans, request)
        data = []

        for loan in page:
            serializer = LoanDetailsSerializer(loan)
            employee = loan.employee
            record = serializer.data

            record['employeename'] = employee.name
            record['total_loan'] = (loan.loan_amount or 0) + (loan.previous_loan or 0)
            record['employee_details'] = {
                'name': employee.name,
                'designation': employee.designation,
                'department': employee.department,
                'mobileno': employee.mobileno,
                'adhaar': employee.adhaar,
                'PAN': employee.PAN
            }

            documents = LoanDocument.objects.filter(employee=employee)
            record['loan_documents'] = [
                {
                    'id': doc.id,
                    'pdf_file': request.build_absolute_uri(doc.pdf_file.url),
                    'uploaded_at': doc.uploaded_at
                }
                for doc in documents
            ]

            data.append(record)

        return paginator.get_paginated_response(data)

    # POST
    elif request.method == 'POST':
        employeename = request.data.get('input_employeename')
        if not employeename:
            return Response({'error': 'input_employeename is required'}, status=400)

        try:
            employee = Employee_profile.objects.get(name__iexact=employeename.strip())
        except Employee_profile.DoesNotExist:
            return Response({'error': 'Employee not found with this name'}, status=404)

        data = request.data.copy()
        data['employee'] = employee.empid  # FK expects empid

        serializer = LoanDetailsSerializer(data=data)
        if serializer.is_valid():
            loan = serializer.save()

            # Update employee total loan
            employee.total_loan_amount += loan.loan_amount or 0
            employee.save()

            response = serializer.data
            response['employeename'] = employee.name
            response['total_loan'] = (loan.loan_amount or 0) + (loan.previous_loan or 0)
            response['employee_details'] = {
                'name': employee.name,
                'designation': employee.designation,
                'department': employee.department,
                'mobileno': employee.mobileno,
                'adhaar': employee.adhaar,
                'PAN': employee.PAN
            }

            return Response({'message': 'Loan created', 'data': response}, status=201)
        return Response(serializer.errors, status=400)

    # PUT
    elif request.method == 'PUT':
        if not loan_id:
            return Response({'error': 'Loan ID is required'}, status=400)
        try:
            loan = LoanDetails.objects.get(pk=loan_id)
        except LoanDetails.DoesNotExist:
            return Response({'error': 'Loan not found'}, status=404)

        old_loan_amount = loan.loan_amount or 0
        serializer = LoanDetailsSerializer(loan, data=request.data, partial=True)

        if serializer.is_valid():
            updated_loan = serializer.save()
            # Update total loan difference
            new_loan_amount = updated_loan.loan_amount or 0
            diff = new_loan_amount - old_loan_amount
            loan.employee.total_loan_amount += diff
            loan.employee.save()

            response = serializer.data
            response['employeename'] = loan.employee.name
            response['total_loan'] = (updated_loan.loan_amount or 0) + (updated_loan.previous_loan or 0)
            response['employee_details'] = {
                'name': loan.employee.name,
                'designation': loan.employee.designation,
                'department': loan.employee.department,
                'mobileno': loan.employee.mobileno,
                'adhaar': loan.employee.adhaar,
                'PAN': loan.employee.PAN
            }

            return Response({'message': 'Loan updated', 'data': response})
        return Response(serializer.errors, status=400)

    # DELETE
    elif request.method == 'DELETE':
        if not loan_id:
            return Response({'error': 'Loan ID is required'}, status=400)
        try:
            loan = LoanDetails.objects.get(pk=loan_id)
            loan.delete()
            return Response({'message': 'Loan deleted successfully'}, status=204)
        except LoanDetails.DoesNotExist:
            return Response({'error': 'Loan not found'}, status=404)
        
@api_view(['GET', 'POST', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def loan_document_api(request):
    doc_id = request.query_params.get('id')

    if request.method == 'GET':
        if doc_id:
            try:
                doc = LoanDocument.objects.get(pk=doc_id)
            except LoanDocument.DoesNotExist:
                return Response({'error': 'Document not found'}, status=404)
            return Response(LoanDocumentSerializer(doc).data)

        docs = LoanDocument.objects.all()
        return Response(LoanDocumentSerializer(docs, many=True).data)


    elif request.method == 'POST':
        # 1) Grab empid from form-data or query-string
        empid = request.data.get('employee') or request.query_params.get('empid')
        # 2) Grab the uploaded file
        pdf = request.FILES.get('pdf_file')

        if not empid or not pdf:
            return Response(
                {'error': 'You must provide employee (empid) and pdf_file.'},
                status=400
            )

        # 3) Make a mutable copy of request.data and ensure employee key is present
        data = request.data.copy()
        data['employee'] = empid

        # 4) Now instantiate the serializer normally—DRF will pull pdf_file from data
        serializer = LoanDocumentSerializer(data=data)

        if not serializer.is_valid():
            # Debug line—remove in production
            print(">> validation errors:", serializer.errors)
            return Response(serializer.errors, status=400)

        # 5) Save and respond
        doc = serializer.save()
        return Response(
            {'message': 'Uploaded successfully', 'data': serializer.data},
            status=201
        )

    elif request.method == 'DELETE':
        if not doc_id:
            return Response({'error': 'id is required for deletion'}, status=400)
        try:
            LoanDocument.objects.get(pk=doc_id).delete()
            return Response(status=204)
        except LoanDocument.DoesNotExist:
            return Response({'error': 'Document not found'}, status=404)
        

class SalaryAPIView(APIView):
    def get(self, request):
        empid = request.query_params.get('empid')
        name = request.query_params.get('name')
        department = request.query_params.get('department')
        designation = request.query_params.get('designation')
        status_filter = request.query_params.get('status')  # 'paid', 'unpaid', 'partial', 'no salary'
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        employees = Employee_profile.objects.all()
        if empid:
            employees = employees.filter(empid__iexact=empid)
        if name:
            employees = employees.filter(name__icontains=name)
        if department:
            employees = employees.filter(department__icontains=department)
        if designation:
            employees = employees.filter(designation__icontains=designation)

        employee_results = []

        for emp in employees:
            salaries = Salary.objects.filter(employee=emp)
            if from_date:
                salaries = salaries.filter(created_at__date__gte=from_date)
            if to_date:
                salaries = salaries.filter(created_at__date__lte=to_date)

            salary_serialized = SalarySerializer(salaries, many=True).data
            filtered_salary = []

            for s in salary_serialized:
                pay = float(s.get('pay') or 0)
                balance = float(s.get('balance') or 0)

                if pay == 0:
                    s['status'] = 'unpaid'
                elif balance == 0:
                    s['status'] = 'paid'
                else:
                    s['status'] = 'partial'

                s['rest_amount'] = 0 if balance == 0 else max(balance - pay, 0)

                if status_filter and s['status'] != status_filter:
                    continue

                filtered_salary.append(s)

            # ✅ Skip if filtering by date and no salary found
            if (from_date or to_date) and not filtered_salary:
                continue

            # Compute status
            computed_status = filtered_salary[-1]['status'] if filtered_salary else 'no salary'

            if status_filter and computed_status != status_filter:
                continue

            latest_loan = LoanDetails.objects.filter(employee=emp).order_by('-date').first()
            loan_serialized = None
            total_loan_amount = 0
            if latest_loan:
                loan_serialized = LoanDetailsSerializer(latest_loan).data
                total = (latest_loan.loan_amount or 0) + (latest_loan.previous_loan or 0)
                loan_serialized['total_loan'] = total
                total_loan_amount = total

            emp_data = {
                "empid": emp.empid,
                "name": emp.name,
                "email": emp.email,
                "mobileno": emp.mobileno,
                "department": emp.department,
                "designation": emp.designation,
                "monthly_salary": emp.monthly_salary,
                "status": emp.status,
                "salary_status": computed_status,
                "salary_details": filtered_salary,
                "loan_details": loan_serialized,
                "total_loan_amount": total_loan_amount,
            }

            employee_results.append(emp_data)
        # Paginate final list
        if not empid:
            paginator = CustomPageNumberPagination()
            paginated_employees = paginator.paginate_queryset(employee_results, request)
            return paginator.get_paginated_response(paginated_employees)
        else:
            return Response(employee_results)

    def post(self, request):
        # Get employee_name from request
        employee_name = request.data.get('employee_name')
        if not employee_name:
            return Response({"error": "employee_name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee_profile.objects.get(name__iexact=employee_name)
        except Employee_profile.DoesNotExist:
            return Response({"error": "Employee with this name does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare data for serializer
        salary_data = request.data.copy()
        salary_data['employee'] = employee.empid  # Use empid for FK assignment
        salary_data.pop('employee_name', None)  # Remove non-model field

        # Logic for auto status
        pay = float(salary_data.get('pay') or 0)
        balance = float(salary_data.get('balance') or 0)

        if pay == 0:
            salary_data['status'] = 'unpaid'
        elif pay == balance:
            salary_data['status'] = 'paid'
        else:
            salary_data['status'] = 'partial'
            

        serializer = SalarySerializer(data=salary_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Salary created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        salary_id = request.query_params.get('id')
        if not salary_id:
            return Response({"error": "Salary ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        salary = get_object_or_404(Salary, id=salary_id)
        salary_data = request.data.copy()

        # Optional: auto-update status on update
        pay = float(salary_data.get('pay') or 0)
        balance = float(salary_data.get('balance') or 0)
        if pay == 0:
            salary_data['status'] = 'pending'
        elif pay == balance:
            salary_data['status'] = 'paid'
        else:
            salary_data['status'] = 'partial'

        serializer = SalarySerializer(salary, data=salary_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Salary updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        salary_id = request.query_params.get('id')
        salary = get_object_or_404(Salary, id=salary_id)
        salary.delete()
        return Response({"message": "Salary deleted"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def salary_document_api(request):
    doc_id = request.query_params.get('id')

    if request.method == 'GET':
        if doc_id:
            try:
                doc = SalaryDocument.objects.get(pk=doc_id)
            except SalaryDocument.DoesNotExist:
                return Response({'error': 'Document not found'}, status=404)
            return Response(SalaryDocumentSerializer(doc).data)

        docs = SalaryDocument.objects.all()
        return Response(SalaryDocumentSerializer(docs, many=True).data)

    elif request.method == 'POST':
        empid = request.data.get('employee') or request.query_params.get('empid')
        pdf = request.FILES.get('pdf_file')

        if not empid or not pdf:
            return Response(
                {'error': 'You must provide employee (empid) and pdf_file.'},
                status=400
            )

        data = request.data.copy()
        data['employee'] = empid

        serializer = SalaryDocumentSerializer(data=data)

        if not serializer.is_valid():
            print(">> validation errors:", serializer.errors)
            return Response(serializer.errors, status=400)

        doc = serializer.save()
        return Response(
            {'message': 'Uploaded successfully', 'data': serializer.data},
            status=201
        )

    elif request.method == 'DELETE':
        if not doc_id:
            return Response({'error': 'id is required for deletion'}, status=400)
        try:
            SalaryDocument.objects.get(pk=doc_id).delete()
            return Response(status=204)
        except SalaryDocument.DoesNotExist:
            return Response({'error': 'Document not found'}, status=404)