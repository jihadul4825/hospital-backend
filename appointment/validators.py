from django.core.exceptions import ValidationError

def validate_appointment_time(doctor, patient, time):
    from .models import Appointment
    # Ensure selected time belongs to doctor
    if doctor and time and not doctor.available_time.filter(id=time.id).exists():
        raise ValidationError({
            "time": f"This time slot ('{time}') is not available for Dr. {doctor.user.first_name}."

        })
        
    # Prevent duplicate appointment
    if Appointment.objects.select_related('patient', 'doctor', 'time').filter(
        doctor=doctor,
        time=time,
        patient=patient,
        cancel=False
    ).exists():
        raise ValidationError({
            "non_field_errors": [
                f"You already have an appointment with Dr. {doctor.user.first_name} at '{time}'."
            ]
        })