from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient
from doctor.models import Doctor, AvailableTime


APPOINTMENT_STATUS = [
    ("pending", "pending"),
    ("approved", "approved"),
    ("Running", "Running"),
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
    time = models.OneToOneField(AvailableTime, on_delete=models.CASCADE)
    cancel = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Patient : {self.patient.user.first_name} {self.patient.user.last_name} | Doctor : {self.doctor.user.first_name} {self.doctor.user.last_name}"

