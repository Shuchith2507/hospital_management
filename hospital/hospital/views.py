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
from django.db.models import Max

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

# myapp/views.py

@api_view(['POST'])
def hospital_onboarding(request):
    serializer = HospitalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def department_management(request, hospital_name):
    try:
        hospital = Hospital.objects.get(name=hospital_name)
    except Hospital.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(hospital=hospital)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def hospital_list(request):
    hospitals = Hospital.objects.all()
    serializer = HospitalSerializer(hospitals, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def department_list(request, hospital_name):
    try:
        hospital = Hospital.objects.get(name=hospital_name)
    except Hospital.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    departments = hospital.departments.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_patient(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def patient_list(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def patient_status_by_name(request, patient_name):
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

from django.db.models import Max,F



@api_view(['GET'])
def patient_visits_details(request, patient_name):
    try:
        visits = (
            Patient.objects
            .filter(name=patient_name)
            .values('hospital__name')
            .annotate(last_visit=Max('entry_datetime'), final_status=F('status'))
        )
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=404)

    z =[]
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

        z.append

    return Response(unique_hospitals)