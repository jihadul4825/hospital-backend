from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Service
from .serializers import ServiceSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
