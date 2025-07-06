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
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.views import APIView

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def employee_profile_api(request):
    empid = request.query_params.get('empid')

    if request.method == 'GET':
        if empid:
            try:
                employee = Employee_profile.objects.get(pk=empid)
                serializer = EmployeeProfileSerializer(employee)
                data = serializer.data

                # Remove top-level total_loan_amount (from model)
                data.pop('total_loan_amount', None)

                # Process loan details: add total_loan and calculate total sum
                total_loan_sum = 0
                for loan in data.get('loan_details', []):
                    loan_amount = loan.get('loan_amount') or 0
                    previous_loan = loan.get('previous_loan') or 0
                    total_loan = loan_amount + previous_loan
                    loan['total_loan'] = total_loan
                    total_loan_sum += total_loan

                data['total_loan_amount'] = total_loan_sum

                # Inject salary_details
                salaries = Salary.objects.filter(employee=employee)
                salary_serializer = SalarySerializer(salaries, many=True)
                salary_data = salary_serializer.data

                # Dynamically update status in GET response
                for sal in salary_data:
                    pay = float(sal.get('pay') or 0)
                    balance = float(sal.get('balance') or 0)
                    if pay == 0:
                        sal['status'] = 'pending'
                    elif pay == balance:
                        sal['status'] = 'paid'
                    else:
                        sal['status'] = 'partial'

                data['salary_details'] = salary_data

                # ✅ Inject salary_documents
                salary_docs = SalaryDocument.objects.filter(employee=employee)
                salary_doc_serializer = SalaryDocumentSerializer(salary_docs, many=True)
                data['salary_documents'] = salary_doc_serializer.data

                return Response(data)

            except Employee_profile.DoesNotExist:
                return Response({'error': 'Employee not found'}, status=404)

        else:
            employees = Employee_profile.objects.all()
            serializer = EmployeeProfileSerializer(employees, many=True)
            data_list = serializer.data

            for data in data_list:
                data.pop('total_loan_amount', None)

                # Process loan details
                total_loan_sum = 0
                for loan in data.get('loan_details', []):
                    loan_amount = loan.get('loan_amount') or 0
                    previous_loan = loan.get('previous_loan') or 0
                    total_loan = loan_amount + previous_loan
                    loan['total_loan'] = total_loan
                    total_loan_sum += total_loan

                data['total_loan_amount'] = total_loan_sum

                # Get employee instance
                try:
                    employee = Employee_profile.objects.get(empid=data['empid'])
                except Employee_profile.DoesNotExist:
                    employee = None

                if employee:
                    # Inject salary_details
                    salaries = Salary.objects.filter(employee=employee)
                    salary_serializer = SalarySerializer(salaries, many=True)
                    salary_data = salary_serializer.data

                    for sal in salary_data:
                        pay = float(sal.get('pay') or 0)
                        balance = float(sal.get('balance') or 0)
                        if pay == 0:
                            sal['status'] = 'pending'
                        elif pay == balance:
                            sal['status'] = 'paid'
                        else:
                            sal['status'] = 'partial'

                    data['salary_details'] = salary_data

                    # ✅ Inject salary_documents
                    salary_docs = SalaryDocument.objects.filter(employee=employee)
                    salary_doc_serializer = SalaryDocumentSerializer(salary_docs, many=True)
                    data['salary_documents'] = salary_doc_serializer.data
                else:
                    data['salary_details'] = []
                    data['salary_documents'] = []

            return Response(data_list)
        
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

    # GET (Single Loan Record)
    if request.method == 'GET':
        if loan_id:
            try:
                loan = LoanDetails.objects.get(pk=loan_id)
            except LoanDetails.DoesNotExist:
                return Response({'error': 'Loan not found'}, status=404)

            employee = loan.employee
            serializer = LoanDetailsSerializer(loan)
            response = serializer.data

            # Employee info
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

            # Loan Documents
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

        # GET (All Loans)
        loans = LoanDetails.objects.all()
        data = []
        for loan in loans:
            serializer = LoanDetailsSerializer(loan)
            employee = loan.employee
            record = serializer.data

            # Employee info
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

            # Loan Documents
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
        return Response(data)

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

        if empid:
            employees = Employee_profile.objects.filter(empid=empid)
        else:
            employees = Employee_profile.objects.all()

        response_data = []

        for emp in employees:
            # === Get Salary Details ===
            salaries = Salary.objects.filter(employee=emp)
            salary_serialized = SalarySerializer(salaries, many=True).data

            for s in salary_serialized:
                pay = float(s.get('pay') or 0)
                balance = float(s.get('balance') or 0)

                # Determine status
                if pay == 0:
                    s['status'] = 'unpaid'
                elif balance == 0:
                    s['status'] = 'paid'
                else:
                    s['status'] = 'partial'

                # Calculate rest_amount
                if balance == 0:
                    s['rest_amount'] = 0
                else:
                    s['rest_amount'] = max(balance - pay, 0)

            # === Get Latest Loan Detail ===
            latest_loan = LoanDetails.objects.filter(employee=emp).order_by('-date').first()
            loan_serialized = None
            total_loan_amount = 0

            if latest_loan:
                loan_serialized = LoanDetailsSerializer(latest_loan).data
                loan_amt = latest_loan.loan_amount or 0
                prev_loan = latest_loan.previous_loan or 0
                total = loan_amt + prev_loan
                loan_serialized['total_loan'] = total
                total_loan_amount = total

            # === Prepare Final Employee Record ===
            emp_data = {
                "empid": emp.empid,
                "name": emp.name,
                "email": emp.email,
                "mobileno": emp.mobileno,
                "department": emp.department,
                "designation": emp.designation,
                "monthly_salary": emp.monthly_salary,
                "status": emp.status,
                "salary_details": salary_serialized,
                "loan_details": loan_serialized,
                "total_loan_amount": total_loan_amount,
            }

            response_data.append(emp_data)

        return Response(response_data)

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