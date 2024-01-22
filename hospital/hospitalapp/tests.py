from django.test import TestCase
from .models import Patient
from datetime import date

class PatientModelTest(TestCase):
    def setUp(self):

        self.patient_data = {
            'name': 'John Doe',
            'gender': 'M',
            'dob': date(1990, 1, 1),
            'ph_num': '1234567890',
        }
        self.patient = Patient.objects.create(**self.patient_data)

    def test_patient_creation(self):
        
        self.assertEqual(self.patient.name, 'John Doe')
        self.assertEqual(self.patient.gender, 'M')
        self.assertEqual(self.patient.dob, date(1990, 1, 1))
        self.assertEqual(self.patient.ph_num, '1234567890')

    def test_gender_choices(self):
        import random

        GENDER_CHOICES = [
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
        ]

        random_gender = random.choice(GENDER_CHOICES)
        patient = Patient.objects.create(name='Test', gender='M', dob=date(2000, 1, 1), ph_num='1234567821')
        self.assertEqual(patient.gender, random_gender[0])

    
    def test_phone_choices(self):
        # try:
        patient1 = Patient.objects.filter(ph_num='1234567890').first()
        self.assertEqual(self.patient, patient1)
        # except:
        #     print(3456789)

