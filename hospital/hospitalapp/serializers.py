from rest_framework import serializers
from .models import Hospital, Department, Patient, Visited

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class PatientSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields=(
            'name','status'
        )

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class VisitedSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name')
    patient_status = serializers.CharField(source='patient.status')
    hospital_name = serializers.CharField(source='hospital.name')

    class Meta:
        model = Visited
        fields = ('patient_name', 'patient_status', 'hospital_name', 'date_time')