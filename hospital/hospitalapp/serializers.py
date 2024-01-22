from rest_framework import serializers
from .models import Hospital, Department, Patient, Appointment, Doctor

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'



def is_phone_valid(value):
    if len(value) < 10:
        raise serializers.ValidationError('Phone number cannot be lesser than 10 digits.')
    elif len(value) > 10:
        raise serializers.ValidationError('Phone number cannot be more than 10 digits.')
    
class PatientSerializer1(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name')
    class Meta:
        model = Appointment
        fields= ['patient_name','status',]

class PatientSerializer(serializers.ModelSerializer):
    ph_num = serializers.CharField(validators=[is_phone_valid])
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentSerializer1(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name')
    hospital_name = serializers.CharField(source='hospital.name')
    department_name = serializers.CharField(source='department.name')
    class Meta:
        model = Appointment
        fields = ['patient_name','hospital_name','department_name','status','date_time']

class DoctorSerializer(serializers.ModelSerializer):
    ph_num = serializers.CharField(validators=[is_phone_valid])
    class Meta:
        model = Doctor
        fields = '__all__'