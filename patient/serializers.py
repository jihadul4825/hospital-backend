from rest_framework import serializers
from .models import Patient, Account
from django.db import transaction



class PatientReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    # first_name = serializers.ReadOnlyField(source='user.first_name')
    # last_name = serializers.ReadOnlyField(source='user.last_name')
    full_name = serializers.ReadOnlyField(source='user.get_full_name')
    
    class Meta:
        model = Patient
        fields = ['id', 'user', 'image', 'mobile_no', 'full_name']


class PatientWriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=False, 
        queryset=Account.objects.filter(is_staff=False, is_superuser=False)
        .exclude(doctor__isnull=False,)
    )
    
    class Meta:
        model = Patient
        fields = ['user', 'image', 'mobile_no']
        
        
    def create(self, validated_data):
        with transaction.atomic():
            return Patient.objects.create(**validated_data)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
            
        
