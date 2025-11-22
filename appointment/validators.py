from django.core.exceptions import ValidationError

def validate_appointment(doctor=None, patient=None, time=None):
    """
        One validator used by BOTH Django Admin and DRF.
    """
    
    errors = {}

    # --- doctor ---
    if not doctor:
        errors["doctor"] = "Please select a doctor."

    # --- patient ---
    if not patient:
        errors["patient"] = "Please select a patient."

    # --- time ---
    if not time:
        errors["time"] = "Please select a time."
    else:
        # validate time belongs to doctor
        if doctor and not doctor.available_time.filter(id=time.id).exists():
            errors["time"] = (
                f"This time '{time}' is not available for Dr. "
                f"{doctor.user.first_name if doctor else ''}."
            )
        
    # Prevent duplicate appointment
    if doctor and patient and time:
        from .models import Appointment
        if Appointment.objects.filter(
            doctor=doctor,
            patient=patient,
            time=time,
            cancel=False
        ).exists():
            errors["non_field_errors"] = [
                f"You already have an appointment at '{time}' with this doctor."
            ]
            
    if errors:
        raise ValidationError(errors)
