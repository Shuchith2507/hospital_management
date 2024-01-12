from django.contrib import admin
from .models import Hospital,Department, Patient, Visited

admin.site.register(Hospital)
admin.site.register(Department)
admin.site.register(Patient)
admin.site.register(Visited)
