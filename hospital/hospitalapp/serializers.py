from rest_framework import serializers
from .models import Student
from .models import Hospital, Department, Patient

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields=(
            'name','address'
        )

class DepartmentSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)

    class Meta:
        model = Department
        fields = ['name', 'hospital_name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=(
            'name','age'
        )

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'