from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    description=models.TextField()
    date_enrolled=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# myapp/models.py

from django.db import models


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # Add unique=True
    address = models.TextField()
    department = models.ManyToManyField(Department)

    def __str__(self):
        return self.name



# class Patient(models.Model):
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#     ]

#     STATUS_CHOICES = [
#         ('PC', 'Primary Check'),
#         ('C', 'Consultation'),
#         ('D', 'Discharged'),
#         ('A', 'Admitted'),
#         ('R', 'Referred'),
#     ]

#     patient_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#     dob = models.DateField()
#     hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE, to_field='name')
#     # disease = models.CharField(max_length=100)
#     doctor_name = models.CharField(max_length=100)
#     status = models.CharField(max_length=2, choices=STATUS_CHOICES)
#     ph_num = models.CharField(len=10,unique=True)
#     # medication = models.TextField(blank=True, null=True)
#     # remarks = models.TextField(blank=True, null=True)
#     entry_datetime = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.patient_id}"



    
class Hospital(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PC', 'Primary Check'),
        ('C', 'Consultation'),
        ('D', 'Discharged'),
        ('A', 'Admitted'),
        ('R', 'Referred'),
    ]

    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=100)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    ph_num = models.CharField(max_length=10, unique=True)
    entry_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.patient_id}"

class Visited(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)