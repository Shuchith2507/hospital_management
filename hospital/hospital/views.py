from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hospitalapp.models import Hospital, Department,Patient, Visited
from hospitalapp.serializers import HospitalSerializer, DepartmentSerializer, PatientSerializer, PatientSerializer1
from datetime import datetime
from django.views import View

from hospitalapp.forms import HospitalForm,PatientForm,DepartmentForm


class MainView(APIView):

    def get(self, request, *args, **kwargs):
        hospitals = Hospital.objects.all()
        patients = Patient.objects.all()

        context = {
            'hospitals': hospitals,
            'patients': patients,
        }

        return render(request, 'main.html', context)


class HospitalViews(View):

    def get(self, request, *args, **kwargs):
        hospitals = Hospital.objects.all()
        return render(request, 'hospital_list.html', {'hospitals': hospitals})

    def post(self, request, *args, **kwargs):
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hospital-list') 
        hospitals = Hospital.objects.all()
        return render(request, 'hospital_list.html', {'hospitals': hospitals, 'form': form})


class DepartmentViews(APIView):
    def get(self, request, hospital_name, *args, **kwargs):
        try:
            hospital = Hospital.objects.get(name=hospital_name)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        departments = hospital.department.all()
        serializer = DepartmentSerializer(departments, many=True)

        return render(request, 'department_list.html', {'departments': serializer.data, 'hospital_name': hospital_name})


class DepartmentAdd(APIView):

    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        return render(request, 'department.html', {'departments': departments})

    def post(self, request, *args, **kwargs):
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department')  
        department = Department.objects.all()
        return render(request, 'department.html', {'department': department, 'form': form})
    

class PatientViews(APIView):

    def get(self, request, *args, **kwargs):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return render(request, 'patient_list.html', {'patients': serializer.data})

    def post(self, request, *args, **kwargs):
        ph_num = request.POST.get('ph_num')
        name = request.POST.get('name')
        form = PatientForm(request.POST)
        if ph_num and name:
            try:
                existing_patient = Patient.objects.get(ph_num=ph_num, name=name)
                if(existing_patient):
                    hos = Hospital.objects.get(hospital_id=request.POST.get('hospital'))
                    existing_patient.dob = request.POST.get('dob')
                    existing_patient.hospital = hos
                    existing_patient.doctor_name = request.POST.get('doctor_name')
                    existing_patient.status = request.POST.get('status')
                    existing_patient.save()


                    
                    Visited.objects.create(
                    patient=existing_patient,
                    date_time=datetime.now(),
                    hospital=hos,
                    )


            except Patient.DoesNotExist:
                form = PatientForm(data=request.POST)
                patient = form.save()
                hos = Hospital.objects.get(hospital_id=request.POST.get('hospital'))
                Visited.objects.create(
                    patient=patient,
                    date_time=datetime.now(),
                    hospital=hos
                    )
            
            return redirect('patient-list')  
        patients = Patient.objects.all()
        return render(request, 'patient_list.html', {'patients': patients, 'form': PatientForm()})


class PatientStatusByName(APIView):
    def get(self, request, patient_name,ph_num, *args, **kwargs):
        try:
            patient = (
                Patient.objects.get(name=patient_name,ph_num=ph_num)
            )
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)

        serializer = PatientSerializer1(patient)
        return render(request, 'patient_status_by_name.html', {'patient': serializer.data, 'patient_name': patient_name})


class PatientVisits(APIView):

    def get(self, request, patient_name,ph_num, *args, **kwargs):
        try:
            patient = (
                Patient.objects.get(name=patient_name,ph_num=ph_num)
            )
            patient_visits = Visited.objects.filter(patient=patient).order_by('-date_time')

        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=404)

        return render(request, 'patient_visits_details.html', {'visits': patient_visits, 'patient_name': patient_name})


# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from hospitalapp.models import Hospital, Department,Patient, Visited
# from hospitalapp.serializers import HospitalSerializer, DepartmentSerializer, PatientSerializer, PatientSerializer1, VisitedSerializer
# from datetime import datetime
# from django.views import View


# class MainView(View):
#     def get(self, request, *args, **kwargs):
#         hospitals = Hospital.objects.all()
#         patients = Patient.objects.all()

#         context = {
#             'hospitals': hospitals,
#             'patients': patients,
#         }

#         return render(request, 'main.html', context)

# class HospitalViews(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = HospitalSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, *args, **kwargs):
#         hospitals = Hospital.objects.all()
#         serializer = HospitalSerializer(hospitals, many=True)
#         return Response(serializer.data)

# class DepartmentViews(APIView):
#     def get(self, request, hospital_name, *args, **kwargs):
#         try:
#             hospital = Hospital.objects.get(name=hospital_name)
#         except Hospital.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         departments = hospital.department.all()
#         serializer = DepartmentSerializer(departments, many=True)
#         return Response(serializer.data)
    
# class DepartmentAdd(APIView):
#     def get(self, request, *args, **kwargs):
#         departments = Department.objects.all()
#         serializer = DepartmentSerializer(departments, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         serializer = DepartmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PatientViews(APIView):
#     def get(self, request, *args, **kwargs):
#         qs=Patient.objects.all()
#         serializer=PatientSerializer(qs,many=True)
#         return Response(serializer.data) 

#     def post(self, request, *args, **kwargs):
#         # request.d
#         ph_num = request.data.get('ph_num')
#         name = request.data.get('name')

#         if(ph_num and name):
#             existing_patient = Patient.objects.get(ph_num=ph_num,name=name)
#             if existing_patient:
#                 serializer = PatientSerializer(existing_patient, data=request.data)
#                 if serializer.is_valid():
#                     serializer.save()

#                 hospital_id = request.data.get('hospital')
#                 hospital = Hospital.objects.get(hospital_id=hospital_id)

#                 Visited.objects.create(
#                     patient=existing_patient,
#                     date_time=datetime.now(),
#                     hospital=hospital
#                 )
                
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response("Please enter phone number and name in datafield")

        
#         serializer = PatientSerializer(data=request.data)
#         if serializer.is_valid():
#             patient = serializer.save()

#             hospital_id = request.data.get('hospital')
#             hospital = Hospital.objects.get(hospital_id=hospital_id)

#             Visited.objects.create(
#                 patient=patient,
#                 date_time=datetime.now(),
#                 hospital=hospital
#             )

#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PatientStatusByName(APIView):
#     def get(self, request, patient_name,ph_num, *args, **kwargs):
#         try:
#             patient = (
#                 Patient.objects.get(name=patient_name,ph_num=ph_num)
#             )
            
#         except Patient.DoesNotExist:
#             return Response({'error': 'Patient not found'}, status=404)

#         serializer = PatientSerializer1(patient)
#         return Response(serializer.data)

# class PatientVisits(APIView):
#     def get(self, request, patient_name,ph_num, *args, **kwargs):
#         try:
#             patient = (
#                 Patient.objects.get(name=patient_name,ph_num=ph_num)
#             )
#             patient_visits = Visited.objects.filter(patient=patient).order_by('-date_time')

#             serializer = VisitedSerializer(patient_visits, many=True)
#             return Response(serializer.data,status=200)

#         except Patient.DoesNotExist:
#             return Response({'error': 'Patient not found'}, status=404)




