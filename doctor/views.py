from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .custom_permissions import IsAdminOrApprovedDoctor, IsAdminOrApprovedDoctorOrReadOnly
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
    
    # permission_classes = [IsAdminOrApprovedDoctorOrReadOnly]   # approach 1

    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrApprovedDoctor]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

        
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DoctorWriteSerializer
        return DoctorReadSerializer
    

class DesignationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrApprovedDoctorOrReadOnly]
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class SpecializationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrApprovedDoctorOrReadOnly]
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


class AvailableTimeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrApprovedDoctorOrReadOnly]
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.select_related('reviewer', 'doctor').all()
    serializer_class = ReviewSerializer
