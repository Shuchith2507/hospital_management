"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import TesView
# from .views import hospital_onboarding, department_management, hospital_list, department_list, create_patient, patient_list, patient_status_by_name, patient_visits_details
from .views import (
    HospitalViews,
    DepartmentViews,
    PatientViews,
    PatientStatusByName,
    PatientVisitsDetails,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/',include('rest_framework.urls')),
    path('',TesView.as_view(),name='test'),

    path('hospital/', HospitalViews.as_view(), name='hospital_views'),
    path('department/<str:hospital_name>/', DepartmentViews.as_view(), name='department_views'),
    path('patient/', PatientViews.as_view(), name='patient_views'),
    path('patient/status/<str:patient_name>/', PatientStatusByName.as_view(), name='patient_status_by_name'),
    path('patient/visits/details/<str:patient_name>/', PatientVisitsDetails.as_view(), name='patient_visits_details'),


]
