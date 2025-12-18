from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .custom_permissions import IsAdminOrApprovedDoctor, IsAdminOrApprovedDoctorOrReadOnly
from rest_framework import viewsets, filters
from .models import Designation, Doctor, Specialization, AvailableTime, Review
from .serializers import (
    SpecializationSerializer,
    DesignationSerializer, 
    AvailableTimeSerializer, 
    ReviewSerializer,
    DoctorReadSerializer,
    DoctorWriteSerializer
)
from .paginator import DoctorPagination
from .custom_filters import AvailableTimeFilter
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend




class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('user').prefetch_related(
        'designation', 'specialization', 'available_time'
    ).all()
    
    # permission_classes = [IsAdminOrApprovedDoctorOrReadOnly]   # approach 1

    
    def get_permissions(self): # approach 2
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrApprovedDoctor]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

        
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DoctorWriteSerializer
        return DoctorReadSerializer
    pagination_class = DoctorPagination
    

class DesignationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrApprovedDoctorOrReadOnly]
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class SpecializationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrApprovedDoctorOrReadOnly]
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


# class SpecificTimeforEachDoctor(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         doctor_id = request.query_params.get('doctor_id')
#         if doctor_id:
#             return queryset.filter(doctor_id=doctor_id)
#         return queryset


# class AvailableTimeViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAdminOrApprovedDoctorOrReadOnly]
#     # queryset = AvailableTime.objects.annotate(doctor_id=F('doctor__id'))
#     serializer_class = AvailableTimeSerializer
#     filter_backends = [SpecificTimeforEachDoctor]


'''
you can see all available times # http://127.0.0.1:8000/doctors/available_time/
you can see the available times for each doctor # http://127.0.0.1:8000/doctors/available_time/?doctor_id=3
'''
class AvailableTimeViewSet(viewsets.ModelViewSet): 
    permission_classes = [IsAdminOrApprovedDoctorOrReadOnly]
    queryset = AvailableTime.objects.prefetch_related('doctor_set').all()
    serializer_class = AvailableTimeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AvailableTimeFilter



class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.select_related('reviewer', 'doctor').all()
    serializer_class = ReviewSerializer
