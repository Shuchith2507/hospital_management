from django.contrib import admin
from .models import Student
from .models import Hospital,Department, Patient
# Register your models here.
admin.site.register(Student)
admin.site.register(Hospital)
admin.site.register(Department)
admin.site.register(Patient)
# class PatientAdmin(admin.ModelAdmin):
#     list_display = ('name', 'hospital', 'status', 'medication', 'remarks')
#     list_filter = ('hospital', 'status')
#     search_fields = ('name', 'doctor_name', 'disease')

# admin.site.register(Patient, PatientAdmin)