from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Appointment



# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor_name', 'time', 'appointment_types', 'appointment_status', 'symptom', 'cancel']
    
    def patient_name(self, obj):
        return obj.patient.user.first_name
    
    def doctor_name(self, obj):
        return obj.doctor.user.first_name
    
    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.appointment_status == 'running' and obj.appointment_types == 'online':
            email_subject = "Your Online Appointment is Running"
            email_body = render_to_string('user/admin_email.html', {'user': obj.patient.user, 'doctor': obj.doctor.user})
            
            email = EmailMultiAlternatives(email_subject, '', from_email=settings.EMAIL_HOST_USER, to=[obj.patient.user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            
    
admin.site.register(Appointment, AppointmentAdmin)