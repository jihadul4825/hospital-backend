from rest_framework import serializers
from .models import Doctor, Specialization, Designation, AvailableTime, Review, Account
from django.db import transaction


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'name']

class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableTime
        fields = ['id', 'name']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


# ---------- Read serializer ---------
class DoctorReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    designation = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    specialization = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    available_time = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'image',
            'designation', 'specialization', 'available_time', 'mobile_no',
            'fee', 'meet_link'
        ]
        
        
#  -------- Write serializer ---------
class DoctorWriteSerializer(serializers.ModelSerializer):
    # show user if user is not patient
    user = serializers.PrimaryKeyRelatedField(
        many=False, 
        queryset=Account.objects.select_related('doctor', 'patient').filter(is_staff=False, is_superuser=False)
        .exclude(patient__isnull=False)
        .exclude(doctor__isnull=False,)
    )
    designation = serializers.PrimaryKeyRelatedField(many=True, queryset=Designation.objects.all())
    specialization = serializers.PrimaryKeyRelatedField(many=True, queryset=Specialization.objects.all())
    available_time = serializers.PrimaryKeyRelatedField(many=True, queryset=AvailableTime.objects.all())

    class Meta:
        model = Doctor
        fields = [
            'user','image', 'designation', 'specialization', 'available_time','mobile_no',
            'fee', 'meet_link'
        ]
        
    
    def validate_user(self, value):
        # If creating, reject any Account that already has a Doctor
        if self.instance is None and hasattr(value, 'doctor'):
            raise serializers.ValidationError("User already has a Doctor")
        
        # If updating, allow the same user but disallow switching to another already-doctor user
        if self.instance is not None and value != self.instance.user and hasattr(value, 'doctor'):
            raise serializers.ValidationError("Selected account already belongs to another doctor.")
        return value 
        
    
    def create(self, validated_data):
        designation = validated_data.pop('designation', [])
        specialization = validated_data.pop('specialization', [])
        available_time = validated_data.pop('available_time', [])
        
        with transaction.atomic():
            doctor = Doctor.objects.create(**validated_data)
            if designation:
                doctor.designation.set(designation)
            if specialization:
                doctor.specialization.set(specialization)
            if available_time:
                doctor.available_time.set(available_time)
            return doctor
        
    @transaction.atomic
    def update(self, instance, validated_data):
        designation = validated_data.pop('designation', None)
        specialization = validated_data.pop('specialization', None)
        available_time = validated_data.pop('available_time', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if designation:
            instance.designation.set(designation)
        if specialization:
            instance.specialization.set(specialization)
        if available_time:
            instance.available_time.set(available_time)
        
        return instance
        
        
        
        

    
    