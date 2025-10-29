from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentReadSerializer, AppointmentWriteSerializer


class AppointmentViewSet(viewsets.ModelViewSet) :
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.select_related(
        'patient__user', 
        'doctor__user', 
        'time'
    ) \
    .prefetch_related(
        'doctor__designation',
        'doctor__specialization',
        'doctor__available_time'
    ).all()
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AppointmentWriteSerializer
        return AppointmentReadSerializer
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient_id')
        doctor_id = self.request.query_params.get('doctor_id')

        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        return queryset
    
    
