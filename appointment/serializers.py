from rest_framework import serializers
from .models import Appointment, Doctor, Patient, AvailableTime
from django.db import transaction
from .validators import validate_appointment_time


class AppointmentReadSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(many=False)
    doctor = serializers.StringRelatedField(many=False)
    time = serializers.StringRelatedField(many=False)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'time', 'appointment_types', 'symptom', 'appointment_status', 'cancel'
        ]
    

class AppointmentWriteSerializer(serializers.ModelSerializer):
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    time = serializers.PrimaryKeyRelatedField(queryset=AvailableTime.objects.all())
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'time', 'appointment_types', 'symptom', 'appointment_status', 'cancel'
        ]
        
    
    def __init__(self, *args, **kwargs):
        """
        Dynamically filter `time` field queryset
        based on the selected doctor (from request data or instance).
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        doctor_id = None

        # Case 1: from request data (POST/PUT)
        if request:
            doctor_id = request.data.get('doctor') or request.query_params.get('doctor')

        # Case 2: when updating an instance
        if not doctor_id and self.instance and self.instance.doctor_id:
            doctor_id = self.instance.doctor_id

        # Set the time field dynamically
        if doctor_id:
            self.fields['time'].queryset = AvailableTime.objects.filter(doctor_id=doctor_id)
        else:
            self.fields['time'].queryset = AvailableTime.objects.none()  # no doctor selected yet


    def validate(self, attrs):
        """
        Ensure selected time exists for the chosen doctor
        and prevent duplicate appointments.
        """
        validate_appointment_time(attrs.get('doctor'), attrs.get('patient'), attrs.get('time'))
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        return Appointment.objects.create(**validated_data)
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

        
