from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from hospitalapp.models import Hospital, Department,Patient, Visited
from hospitalapp.serializers import HospitalSerializer, DepartmentSerializer, PatientSerializer, PatientSerializer1
from datetime import datetime
from django.db.models import Max,F


class HospitalViews(APIView):
    def post(self, request, *args, **kwargs):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

class DepartmentViews(APIView):
    def get(self, request, hospital_name, *args, **kwargs):
        try:
            hospital = Hospital.objects.get(name=hospital_name)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        departments = hospital.department.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

class PatientViews(APIView):
    def get(self, request, *args, **kwargs):
        qs=Patient.objects.all()
        serializer=PatientSerializer(qs,many=True)
        return Response(serializer.data) 

    def post(self, request, *args, **kwargs):
        ph_num = request.data.get('ph_num')

        # Check if the patient already exists based on phone number (ph_num)
        existing_patient = Patient.objects.filter(ph_num=ph_num).first()

        if existing_patient:
            # Patient already exists, update the details in the patient table
            serializer = PatientSerializer(existing_patient, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

            # Make a new entry in the visited table
            hospital_id = request.data.get('hospital')
            hospital = Hospital.objects.get(hospital_id=hospital_id)

            Visited.objects.create(
                patient=existing_patient,
                date_time=datetime.now(),
                hospital=hospital
            )
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Patient doesn't exist, create a new patient and record the first visit
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()

            # Record the first visit
            hospital_id = request.data.get('hospital')
            hospital = Hospital.objects.get(hospital_id=hospital_id)

            Visited.objects.create(
                patient=patient,
                date_time=datetime.now(),
                hospital=hospital
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientStatusByName(APIView):
    def get(self, request, patient_name, *args, **kwargs):
        try:
            patient = (
                Patient.objects
                .filter(name=patient_name)
                .order_by('-entry_datetime') 
                .first() 
            )
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)

        serializer = PatientSerializer1(patient)
        return Response(serializer.data)

class PatientVisitsDetails(APIView):
    def get(self, request, patient_name, *args, **kwargs):
        try:
            # Retrieve all visits from the Visited table for the patient
            visits = (
                Visited.objects
                .filter(patient__name=patient_name)
                .select_related('hospital', 'patient')
                .values('hospital__name', 'patient__status', 'date_time')
                .annotate(final_status=F('patient__status'))
                .order_by('-date_time')
            )
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)

        unique_hospitals = []
        for visit in visits:
            hospital_name = visit['hospital__name']
            last_visit = visit['date_time']
            final_status = visit['final_status']

            unique_hospitals.append({
                'hospital_name': hospital_name,
                'last_visit': last_visit,
                'final_status': final_status,
            })

        return Response(unique_hospitals)


# from django.shortcuts import render, get_object_or_404
# from django.views import View
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view
# from django.urls import reverse
# from hospitalapp.models import Hospital, Department, Patient, Visited
# from hospitalapp.serializers import HospitalSerializer, DepartmentSerializer, PatientSerializer, PatientSerializer1
# from datetime import datetime
# from django.db.models import Max, F

# class HospitalViews(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = HospitalSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, *args, **kwargs):
#         hospitals = Hospital.objects.all()
#         serializer = HospitalSerializer(hospitals, many=True)
        
#         # Rendering HTML directly within the view
#         return render(request, 'hospital_list.html', {'hospitals': serializer.data})

# class DepartmentViews(APIView):
#     def post(self, request, hospital_name, *args, **kwargs):
#         try:
#             hospital = Hospital.objects.get(name=hospital_name)
#         except Hospital.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = DepartmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(hospital=hospital)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, hospital_name, *args, **kwargs):
#         try:
#             hospital = Hospital.objects.get(name=hospital_name)
#         except Hospital.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         departments = hospital.department.all()
#         serializer = DepartmentSerializer(departments, many=True)
#         return render(request, 'department_list.html', {'departments': serializer.data})

# class PatientViews(APIView):
#     def get(self, request, *args, **kwargs):
#         qs = Patient.objects.all()
#         serializer = PatientSerializer(qs, many=True)
#         return render(request, 'patient_list.html', {'patients': serializer.data})

#     def post(self, request, *args, **kwargs):
#         ph_num = request.data.get('ph_num')

#         # Check if the patient already exists based on phone number (ph_num)
#         existing_patient = Patient.objects.filter(ph_num=ph_num).first()

#         if existing_patient:
#             # Patient already exists, update the details in the patient table
#             serializer = PatientSerializer(existing_patient, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()

#             # Make a new entry in the visited table
#             hospital_name = request.data.get('hospital')
#             hospital = Hospital.objects.get(hospital_id=hospital_name)

#             Visited.objects.create(
#                 patient=existing_patient,
#                 date_time=datetime.now(),
#                 hospital=hospital
#             )

#             return render(request, 'patient_list.html', {'patients': serializer.data})

#         # Patient doesn't exist, create a new patient and record the first visit
#         serializer = PatientSerializer(data=request.data)
#         if serializer.is_valid():
#             patient = serializer.save()

#             # Record the first visit
#             hospital_name = request.data.get('hospital')
#             hospital = Hospital.objects.get(name=hospital_name)

#             Visited.objects.create(
#                 patient=patient,
#                 date_time=datetime.now(),
#                 hospital=hospital
#             )

#             return render(request, 'patient_list.html', {'patients': serializer.data})

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PatientStatusByName(APIView):
#     def get(self, request, patient_name, *args, **kwargs):
#         try:
#             patient = (
#                 Patient.objects
#                 .filter(name=patient_name)
#                 .order_by('-entry_datetime')
#                 .first()
#             )
#         except Patient.DoesNotExist:
#             return Response({'error': 'Patient not found'}, status=404)

#         serializer = PatientSerializer1(patient)
#         return render(request, 'patient_details.html', {'patient': serializer.data})

# class PatientVisitsDetails(APIView):
#     def get(self, request, patient_name, *args, **kwargs):
#         try:
#             # Retrieve all visits from the Visited table for the patient
#             visits = (
#                 Visited.objects
#                 .filter(patient__name=patient_name)
#                 .select_related('hospital', 'patient')
#                 .values('hospital__name', 'patient__status', 'date_time')
#                 .annotate(final_status=F('patient__status'))
#                 .order_by('-date_time')
#             )
#         except Patient.DoesNotExist:
#             return Response({'error': 'Patient not found'}, status=404)

#         unique_hospitals = []
#         for visit in visits:
#             hospital_name = visit['hospital__name']
#             last_visit = visit['date_time']
#             final_status = visit['final_status']

#             unique_hospitals.append({
#                 'hospital_name': hospital_name,
#                 'last_visit': last_visit,
#                 'final_status': final_status,
#             })

#         return render(request, 'patient_visits_details.html', {'unique_hospitals': unique_hospitals})