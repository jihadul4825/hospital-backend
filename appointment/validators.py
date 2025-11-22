from django.core.exceptions import ValidationError

def validate_appointment(doctor=None, patient=None, time=None, instance=None):
    """
    One validator used by BOTH Django Admin and DRF.
    """
    
    # Check required fields
    if not doctor:
        raise ValidationError("Please select a doctor.")
    
    if not patient:
        raise ValidationError("Please select a patient.")
    
    if not time:
        raise ValidationError("Please select a time.")
    
    # Check if time belongs to doctor
    if not doctor.available_time.filter(id=time.id).exists():
        raise ValidationError(
            f"This time '{time}' is not available for Dr. {doctor.user.first_name}."
        )
    
    # Check for duplicate appointments - EXCLUDE CURRENT INSTANCE
    from .models import Appointment
    queryset =  Appointment.objects.filter(
        doctor=doctor,
        patient=patient,
        time=time,
        cancel=False
    )
    
    # Exclude the current instance if we're updating an existing appointment
    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    
    if queryset.exists():
        raise ValidationError(
            f"You already have an appointment at '{time}' with this doctor."
        )
        