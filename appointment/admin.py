from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.forms import ModelForm

from .models import Appointment
from doctor.models import Doctor


# -----------------------------
#  Custom Admin Form
# -----------------------------

class AppointmentAdminForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        
        def clean(self):
            cleaned_data = super().clean()
            
            doctor = cleaned_data.get('doctor')
            patient = cleaned_data.get('patient')
            time = cleaned_data.get('time')
            
            # Only validate if all 3 fields are present.
            if doctor and patient and time:
                from .validators import validate_appointment
                validate_appointment(
                    doctor=doctor,
                    patient=patient,
                    time=time,
                )
            
            return cleaned_data

            
# -----------------------------
#  Admin Class
# -----------------------------
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor_name', 'time', 'appointment_types', 'appointment_status', 'symptom', 'cancel']
    

    def patient_name(self, obj):
        return obj.patient.user.first_name

    def doctor_name(self, obj):
        return obj.doctor.user.first_name
   
    # ---- Filter time slots based on selected doctor ----
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "time":
            doctor_id = (
                request.POST.get("doctor")
                or request.GET.get("doctor")
            )
            
            if doctor_id:
                try:
                    doctor = Doctor.objects.get(id=doctor_id)
                    kwargs["queryset"] = doctor.available_time.all()
                except Doctor.DoesNotExist:
                    kwargs["queryset"] = Appointment.objects.none()
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
    # ---------------------------------------------
    # SEND EMAIL WHEN ONLINE APPOINTMENT IS RUNNING
    # ---------------------------------------------
    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.appointment_status == 'running' and obj.appointment_types == 'online':
            email_subject = "Your Online Appointment is Running"
            email_body = render_to_string('appointment/admin_email.html', {'user': obj.patient.user, 'doctor': obj.doctor.user})
            
            email = EmailMultiAlternatives(email_subject, '', from_email=settings.EMAIL_HOST_USER, to=[obj.patient.user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            
    
admin.site.register(Appointment, AppointmentAdmin)