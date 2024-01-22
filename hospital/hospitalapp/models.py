from django.db import models
    
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=200, unique=True) 
    address = models.TextField()
    department = models.ManyToManyField(Department)

    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    hospital = models.ManyToManyField(Hospital)
    ph_num = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
   

class Patient(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other'),]
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    ph_num = models.CharField(max_length=10)
    def __str__(self):
        return self.name

    
class Appointment(models.Model):
    STATUS_CHOICES = [('PC', 'Primary Check'), ('C', 'Consultation'), ('D', 'Discharged'), ('A', 'Admitted'), ('R', 'Referred'),]
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)
    hospital = models.ForeignKey(Hospital, on_delete=models.DO_NOTHING)
    doctor = models.ForeignKey(Doctor,on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    date_time = models.DateTimeField()







