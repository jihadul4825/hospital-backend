from django.shortcuts import render
from rest_framework import viewsets
from .models import Patient
from .serializers import PatientReadSerializer, PatientWriteSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PatientWriteSerializer
        return PatientReadSerializer
    
