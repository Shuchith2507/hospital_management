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
from .views import hospital_onboarding, department_management, hospital_list, department_list, create_patient, patient_list, patient_status_by_name, patient_visits_details



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/',include('rest_framework.urls')),
    path('',TesView.as_view(),name='test'),
    path('hospital/onboarding/', hospital_onboarding, name='hospital_onboarding'),
    path('hospital/<str:hospital_name>/departments/', department_management, name='department_management'),
    path('hospitals/', hospital_list, name='hospital_list'),
    path('hospital/<str:hospital_name>/departments/list/', department_list, name='department_list'),
    path('patient/create/', create_patient, name='create_patient'),
    path('patients/', patient_list, name='patient_list'),
    path('patient/status/<str:patient_name>/', patient_status_by_name, name='patient_status_by_name'),
    path('patient/visits/details/<str:patient_name>/', patient_visits_details, name='patient_visits_details'),
]
