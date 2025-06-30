from django.contrib import admin
from django.urls import path, include
from System_Admin import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('system_company_details_handler/', views.company_detail_api, name='system_company_details_handler'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)