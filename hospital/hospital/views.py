from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from hospitalapp.models import Hospital, Department,Patient
from hospitalapp.serializers import HospitalSerializer, DepartmentSerializer, PatientSerializer

from hospitalapp.serializers import StudentSerializer
from hospitalapp.models import Student
from django.db.models import Max,F

class TesView(APIView):


    # permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        qs=Student.objects.all()
        serializer=StudentSerializer(qs,many=True)
        return Response(serializer.data) 
    
    def post(self, request, *args, **kwargs):
        serializer=StudentSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)




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
    def post(self, request, hospital_name, *args, **kwargs):
        try:
            hospital = Hospital.objects.get(name=hospital_name)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hospital=hospital)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, hospital_name, *args, **kwargs):
        try:
            hospital = Hospital.objects.get(name=hospital_name)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        departments = hospital.department.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

class PatientViews(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def put(self, request, patient_name, *args, **kwargs):
        try:
            patient = Patient.objects.get(name=patient_name)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientStatusByName(APIView):
    def get(self, request, patient_name, *args, **kwargs):
        try:
            patient = (
                Patient.objects
                .filter(name=patient_name)
                .order_by('-entry_datetime')  # Order by entry_datetime in descending order
                .first()  # Select the most recent entry
            )
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)

        serializer = PatientSerializer(patient)
        return Response(serializer.data)

class PatientVisitsDetails(APIView):
    def get(self, request, patient_name, *args, **kwargs):
        try:
            visits = (
                Patient.objects
                .filter(name=patient_name)
                .values('hospital__name')
                .annotate(last_visit=Max('entry_datetime'), final_status=F('status'))
            )
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)

        unique_hospitals = []
        for visit in visits:
            hospital_name = visit['hospital__name']
            last_visit = visit['last_visit']
            final_status = visit['final_status']

            unique_hospitals.append({
                'hospital_name': hospital_name,
                'last_visit': last_visit,
                'final_status': final_status,
            })

        return Response(unique_hospitals)