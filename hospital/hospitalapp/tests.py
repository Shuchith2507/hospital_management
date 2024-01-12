from django.test import TestCase
from .models import Patient, Hospital
from datetime import date
from django.urls import reverse

class PatientModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(name='XXX', address='asdfghjk')

        self.patient_data = {
            'name': 'John Doe',
            'gender': 'M',
            'dob': date(1990, 1, 1),
            'hospital': self.hospital,
            'doctor_name': 'Dr. Smith',
            'status': 'PC',
            'ph_num': '1234567890',
        }

    def test_patient_creation(self):
        patient = Patient.objects.create(**self.patient_data)
        self.assertEqual(patient.name, 'John Doe')
        self.assertEqual(patient.gender, 'M')
        self.assertEqual(patient.dob, date(1990, 1, 1))
        self.assertEqual(patient.hospital, self.hospital)
        self.assertEqual(patient.doctor_name, 'Dr. Smith')
        self.assertEqual(patient.status, 'PC')
        self.assertEqual(patient.ph_num, '1234567890')
        self.assertIsNotNone(patient.entry_datetime)

    def test_gender_choices(self):
        import random

        GENDER_CHOICES = [
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
        ]

        random_gender = random.choice(GENDER_CHOICES)
        patient = Patient.objects.create(name='Test', gender='M', dob=date(2000, 1, 1), hospital=self.hospital, doctor_name='Dr. Test', status='PC', ph_num='1234567821')
        self.assertEqual(patient.gender, random_gender[0])

    def test_unique_phone_number(self):
        Patient.objects.create(**self.patient_data) 
        with self.assertRaises(Exception):
            Patient.objects.create(**self.patient_data)

    # def test_patient_creation_status_code(self):
    #     url = reverse('patient_views')  # Change 'patient_create' to your actual URL name
    #     print(url)
    #     response = self.client.post(url, data=self.patient_data)
    #     print(response)
    #     self.assertEqual(response.status_code, 400)
            
    def tearDown(self):
        pass
