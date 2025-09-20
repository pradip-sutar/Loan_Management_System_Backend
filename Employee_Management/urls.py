from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('employee_management_handler/', employee_profile_api, name='employee_management'),
    path('loan-details/', loan_details_api, name='loan_details'),
    path('loan-documents/', loan_document_api),
    path('salary/', SalaryAPIView.as_view(), name='salary-api'),
    path('salary_documents/', salary_document_api, name='salary_document_api'),

    path('emp-eligible/', EmployeeLoanEligibilityAPIView.as_view(), name='salary-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  #this is the urls.py
