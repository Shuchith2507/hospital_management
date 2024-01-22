# from django.shortcuts import render, redirect
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from hospitalapp.models import Hospital, Department,Patient, Appointment, Doctor
# from hospitalapp.serializers import HospitalSerializer, DepartmentSerializer, PatientSerializer, PatientSerializer1, AppointmentSerializer, AppointmentSerializer1, DoctorSerializer
# from datetime import datetime
# from django.views import View

# from hospitalapp.forms import HospitalForm,PatientForm,DepartmentForm,DoctorForm,AppointmentForm
# from django.core.paginator import Paginator

# class MainView(APIView):

#     def get(self, request, *args, **kwargs):
#         hospitals = Hospital.objects.all()
#         patients = Patient.objects.all()

#         context = {
#             'hospitals': hospitals,
#             'patients': patients,
#         }

#         return render(request, 'main.html', context)


# class HospitalViews(View):

#     def get(self, request, *args, **kwargs):
#         hospitals = Hospital.objects.all()
#         paginator = Paginator(hospitals, 2)

#         page_number = request.GET.get("page")
#         hospitals = paginator.get_page(page_number)
#         return render(request, "hospital_list.html", {"hospitals": hospitals})
#         # return render(request, 'hospital_list.html', {'hospitals': hospitals})

#     def post(self, request, *args, **kwargs):
#         form = HospitalForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('hospital-list') 
#         hospitals = Hospital.objects.all()
#         return render(request, 'hospital_list.html', {'hospitals': hospitals, 'form': form})


# class DepartmentViews(APIView):
#     def get(self, request, hospital_name, *args, **kwargs):
#         try:
#             hospital = Hospital.objects.get(name=hospital_name)
#         except Hospital.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         departments = hospital.department.all()
#         serializer = DepartmentSerializer(departments, many=True)

#         return render(request, 'department_list.html', {'departments': serializer.data, 'hospital_name': hospital_name})


# class DepartmentAdd(APIView):
#     def get(self, request, *args, **kwargs):
#         departments = Department.objects.all()
#         paginator = Paginator(departments, 2)

#         page_number = request.GET.get("page")
#         departments = paginator.get_page(page_number)
#         return render(request, 'department.html', {'departments': departments})

#     def post(self, request, *args, **kwargs):
#         form = DepartmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('department')  
#         departments = Department.objects.all()
#         return render(request, 'department.html', {'departments': departments, 'form': form})
    

# class DoctorViews(APIView):
#     def get(self,request,*args, **kwargs):
#         doctors = Doctor.objects.all()
#         paginator = Paginator(doctors, 2)

#         page_number = request.GET.get("page")
#         doctors = paginator.get_page(page_number)
#         return render(request, 'doctor_list.html', {'doctors': doctors})

    
#     def post(self, request, *args, **kwargs):
#         form = DoctorForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('doctor-list')  
#         doctors = Doctor.objects.all()
#         return render(request, 'doctor_list.html', {'doctors': doctors, 'form': form})

# class AppointmentViews(APIView):
#     def get(self,request,*args, **kwargs):
#         appointments = Appointment.objects.all()
#         import logging
#         logging.warning(appointments)
#         paginator = Paginator(appointments, 5)

#         page_number = request.GET.get("page")
#         appointments = paginator.get_page(page_number)
#         return render(request, 'appointment_list.html', {'appointments': appointments})
    
#     def post(self, request, *args, **kwargs):
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('appointment-list')  
#         appointments = Appointment.objects.all()
#         return render(request, 'appointment_list.html', {'appointments': appointments, 'form': form})


# class PatientViews(APIView):
#     def get(self, request, *args, **kwargs):

#         patients = Patient.objects.all()
#         paginator = Paginator(patients, 2)

#         page_number = request.GET.get("page")
#         patients = paginator.get_page(page_number)
#         return render(request, 'patient_list.html', {'patients': patients})

#     def post(self, request, *args, **kwargs):

#         form = PatientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('patient-list')  
#         patients = Patient.objects.all()
#         return render(request, 'patient_list.html', {'patients': patients, 'form': form})
#         # ph_num = request.POST.get('ph_num')
#         # name = request.POST.get('name')
#         # form = PatientForm(request.POST)
#         # if ph_num and name:
#         #     try:
#         #         existing_patient = Patient.objects.get(ph_num=ph_num, name=name)
#         #         if(existing_patient):
#         #             hos = Hospital.objects.get(hospital_id=request.POST.get('hospital'))
#         #             existing_patient.dob = request.POST.get('dob')
#         #             existing_patient.hospital = hos
#         #             existing_patient.doctor_name = request.POST.get('doctor_name')
#         #             existing_patient.status = request.POST.get('status')
#         #             existing_patient.save()


                    
#         #             Appointment.objects.create(
#         #             patient=existing_patient,
#         #             date_time=datetime.now(),
#         #             hospital=hos,
#         #             )


#         #     except Patient.DoesNotExist:
#         #         form = PatientForm(data=request.POST)
#         #         patient = form.save()
#         #         hos = Hospital.objects.get(hospital_id=request.POST.get('hospital'))
#         #         Appointment.objects.create(
#         #             patient=patient,
#         #             date_time=datetime.now(),
#         #             hospital=hos
#         #             )
            
#         #     return redirect('patient-list')  
#         # patients = Patient.objects.all()
#         # return render(request, 'patient_list.html', {'patients': patients, 'form': PatientForm()})


# class PatientStatusByName(APIView):
#     def get(self, request, patient_name,ph_num, *args, **kwargs):
#         try:
#             patient = (
#                 Patient.objects.get(name=patient_name,ph_num=ph_num)
#             )

#             patient_status = Appointment.objects.filter(patient=patient).order_by('-date_time').first()

#         except Patient.DoesNotExist:
#             return Response({'error': 'Patient not found'}, status=404)

#         serializer = PatientSerializer1(patient)
#         return render(request, 'patient_status_by_name.html', {'patients': patient_status, 'patient_name': patient_name})


# class PatientVisits(APIView):

#     def get(self, request, patient_name,ph_num, *args, **kwargs):
#         try:
#             patient = (
#                 Patient.objects.get(name=patient_name,ph_num=ph_num)
#             )
#             patient_visits = Appointment.objects.filter(patient=patient).order_by('-date_time')
#             paginator = Paginator(patient_visits, 2)

#             page_number = request.GET.get("page")
#             patient_visits = paginator.get_page(page_number)

#         except Patient.DoesNotExist:
#             return Response({'error': 'Patient not found'}, status=404)

#         return render(request, 'patient_visits_details.html', {'patient_visits': patient_visits, 'patient_name': patient_name})


    


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hospitalapp.models import Hospital, Department,Patient, Appointment, Doctor
from hospitalapp.serializers import HospitalSerializer, DepartmentSerializer, PatientSerializer, PatientSerializer1,AppointmentSerializer, DoctorSerializer, AppointmentSerializer1
from datetime import datetime
from django.views import View
import logging

class MainView(View):
    def get(self, request, *args, **kwargs):
        hospitals = Hospital.objects.all()
        patients = Patient.objects.all()


        context = {
            'hospitals': hospitals,
            'patients': patients,
        }

        return Response()

class HospitalViews(APIView):
    def post(self, request, *args, **kwargs):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        logging.warning(serializer.data)
        return Response(serializer.data)

class DepartmentViews(APIView):
    def get(self, request, hospital_name, *args, **kwargs):
        try:
            hospital = Hospital.objects.get(name=hospital_name)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        departments = hospital.department.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
class DepartmentAdd(APIView):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientViews(APIView):
    def get(self, request, *args, **kwargs):
        qs=Patient.objects.all()
        serializer=PatientSerializer(qs,many=True)
        return Response(serializer.data) 

    def post(self, request, *args, **kwargs):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DoctorViews(APIView):
    def get(self,request,*args, **kwargs):
        qs = Doctor.objects.all()
        serializer=DoctorSerializer(qs,many=True)
        return Response(serializer.data) 
    
    def post(self, request, *args, **kwargs):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppointmentViews(APIView):
    def get(self,request,*args, **kwargs):
        qs = Appointment.objects.all()
        serializer=AppointmentSerializer(qs,many=True)
        return Response(serializer.data) 
    
    def post(self, request, *args, **kwargs):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientStatusByName(APIView):
    def get(self, request, patient_name,ph_num, *args, **kwargs):
        try:
            patient = (
                Patient.objects.get(name=patient_name,ph_num=ph_num)
            )

            patient_status = Appointment.objects.filter(patient=patient).order_by('-date_time').first()
            serializer = PatientSerializer1(patient_status)
            return Response(serializer.data)
            
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)

        

class PatientVisits(APIView):
    def get(self, request, patient_name,ph_num, *args, **kwargs):
        try:
            patient = (
                Patient.objects.get(name=patient_name,ph_num=ph_num)
            )
            patient_visits = Appointment.objects.filter(patient=patient).order_by('-date_time')

            serializer = AppointmentSerializer1(patient_visits, many=True)
            return Response(serializer.data,status=200)

        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)

class HospitalName(APIView):
    def get(self, request, hospital_name, *args, **kwargs):
        try:
            doctor = (
                doctors.objects.all()
            )

            hospital = Hospital.objects.get(name=hospital_name)

            serializer = AppointmentSerializer1(patient_visits, many=True)
            return Response(serializer.data,status=200)

        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)



