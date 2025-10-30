from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Doctor, DoctorApproval

@receiver(post_save, sender=Doctor)
def create_doctor_approval(sender, instance, created, **kwargs):
    if created:
        DoctorApproval.objects.get_or_create(doctor=instance)