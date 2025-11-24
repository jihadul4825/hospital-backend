# from django.db import models
# from patient.models import Patient
# from doctor.models import Doctor, AvailableTime
# from .validators import validate_appointment


# APPOINTMENT_STATUS = [
#     ("pending", "pending"),
#     ("approved", "approved"),
#     ("running", "running"),
# ]

# APPOINTMENT_TYPES = [
#     ("online", "online"),
#     ("offline", "offline"),
# ]
# class Appointment(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     appointment_types = models.CharField(choices=APPOINTMENT_TYPES, max_length=10)
#     appointment_status = models.CharField(choices=APPOINTMENT_STATUS, max_length=10, default="pending")
#     symptom = models.TextField()
#     time = models.ForeignKey(AvailableTime, on_delete=models.SET_NULL, null = True, blank = True)
#     cancel = models.BooleanField(default=False)
    
    
#     def clean(self):
#         # Skip validation when fields are missing (during admin's first clean)
#         if not self.doctor or not self.patient or not self.time:
#             return 
            
#         validate_appointment(
#             doctor=self.doctor,
#             patient=self.patient,
#             time=self.time
#         )
    
    
#     def __str__(self):
#         patient_name = (
#             f"{self.patient.user.first_name} {self.patient.user.last_name}"
#             if self.patient else "Unknown Patient"
#         )

#         doctor_name = (
#             f"{self.doctor.user.first_name} {self.doctor.user.last_name}"
#             if self.doctor else "Unknown Doctor"
#         )

#         return f"Patient: {patient_name} | Doctor: {doctor_name}"


from django.db import models
from patient.models import Patient
from doctor.models import Doctor, AvailableTime
from .validators import validate_appointment
from django.core.exceptions import ValidationError

APPOINTMENT_STATUS = [
    ("pending", "pending"),
    ("approved", "approved"),
    ("running", "running"),
]

APPOINTMENT_TYPES = [
    ("online", "online"),
    ("offline", "offline"),
]

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_types = models.CharField(choices=APPOINTMENT_TYPES, max_length=10)
    appointment_status = models.CharField(choices=APPOINTMENT_STATUS, max_length=10, default="pending")
    symptom = models.TextField()
    time = models.ForeignKey(AvailableTime, on_delete=models.SET_NULL, null=True, blank=True)
    cancel = models.BooleanField(default=False)
    
    def clean(self):
        # Skip validation when required fields are missing
        if not hasattr(self, 'doctor') or not self.doctor:
            return
        if not hasattr(self, 'patient') or not self.patient:
            return  
        if not hasattr(self, 'time') or not self.time:
            return
            
        try:
            validate_appointment(
                doctor=self.doctor,
                patient=self.patient,
                time=self.time,
                instance=self # pass the the current instance
            )
        except ValidationError as e:
            raise e
    
    def __str__(self):
        try:
            patient_name = f"{self.patient.user.first_name} {self.patient.user.last_name}"
        except:
            patient_name = "Unknown Patient"

        try:
            doctor_name = f"{self.doctor.user.first_name} {self.doctor.user.last_name}"
        except:
            doctor_name = "Unknown Doctor"

        return f"Patient: {patient_name} | Doctor: {doctor_name}"        