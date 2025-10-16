from rest_framework import serializers
from .models import Appointment, Doctor, Patient, AvailableTime
from django.db import transaction


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
    patient = serializers.PrimaryKeyRelatedField(many=False, queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(many=False, queryset=Doctor.objects.all())
    time = serializers.PrimaryKeyRelatedField(
    many=False,
    queryset=AvailableTime.objects.all()
)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'time', 'appointment_types', 'symptom', 'appointment_status', 'cancel'
        ]


    def validate(self, attrs):
        """
        Custom validation logic:
        - Only allow selecting times available for that doctor.
        - Prevent duplicate appointments (same doctor, same time, same patient).
        """
        doctor = attrs.get('doctor')
        patient = attrs.get('patient')
        time = attrs.get('time')
        
       # Ensure the chosen time is one of the doctor's available times
        if not doctor.available_time.filter(id=time.id).exists():
            raise serializers.ValidationError({
                "time": f"This time slot ('{time}') is not available for Dr. {doctor.user.first_name}."
            })
        
        
        # Prevent duplicate appointment with same doctor & time
        if Appointment.objects.filter(doctor=doctor, time=time, patient=patient, cancel=False).exists():
            raise serializers.ValidationError({
                "non_field_errors": [
                    f"You already have an appointment with Dr. {doctor.user.first_name} at '{time}'."
                ]
            })
        
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
        

