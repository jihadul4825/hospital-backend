from django.shortcuts import render
from .models import Account
from .serializers import AccountSerializer
from rest_framework import generics


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = AccountSerializer
    

