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
from .views import (HospitalViews,DepartmentViews, PatientViews, PatientStatusByName,MainView,DepartmentAdd, PatientVisits, DoctorViews, AppointmentViews)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/',include('rest_framework.urls')),
    path('',include('authenticate.urls')),
    path('home/', MainView.as_view(), name='main'),
    path('hospital/', HospitalViews.as_view(), name='hospital-list'),
    path('department/', DepartmentAdd.as_view(), name='department'),
    path('departments/<str:hospital_name>/', DepartmentViews.as_view(), name='department-list'),
    path('patient/', PatientViews.as_view(), name='patient-list'),
    path('patient_status/<str:patient_name>/<str:ph_num>/', PatientStatusByName.as_view(), name='patient-status-by-name'),
    path('patient_visits/<str:patient_name>/<str:ph_num>/', PatientVisits.as_view(), name='patient-visits-details'),
    path('doctor/',DoctorViews.as_view(),name='doctor-list'),
    path('appointment/',AppointmentViews.as_view(),name='appointment-list')
]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api-auth/',include('rest_framework.urls')),
#     path('hospital/', HospitalViews.as_view(), name='hospital-list'),
#     path('department/', DepartmentAdd.as_view(), name='department'),
#     path('departments/<str:hospital_name>/', DepartmentViews.as_view(), name='department-list'),
#     path('patient/', PatientViews.as_view(), name='patient-list'),
#     path('patient_status/<str:patient_name>/<str:ph_num>/', PatientStatusByName.as_view(), name='patient-status-by-name'),
#     path('patient_visits/<str:patient_name>/<str:ph_num>/', PatientVisits.as_view(), name='patient-visits-details'),
# ]



