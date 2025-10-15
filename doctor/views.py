# views.py
from rest_framework import viewsets
from .models import Designation, Doctor, Specialization, AvailableTime, Review
from .serializers import (
    SpecializationSerializer,
    DesignationSerializer, 
    AvailableTimeSerializer, 
    ReviewSerializer,
    DoctorReadSerializer,
    DoctorWriteSerializer
)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('user').prefetch_related(
        'designation', 'specialization', 'available_time'
    ).all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DoctorWriteSerializer
        return DoctorReadSerializer
    

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


class AvailableTimeViewSet(viewsets.ModelViewSet):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('reviewer', 'doctor').all()
    serializer_class = ReviewSerializer
