from django import forms
from .models import Hospital,Patient, Department, Doctor, Appointment

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'  

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'  

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentForm1(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'