# from django.contrib import admin
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings
# from django.forms import ModelForm

# from .models import Appointment
# from doctor.models import Doctor


# # -----------------------------
# #  Custom Admin Form
# # -----------------------------

# class AppointmentAdminForm(ModelForm):
#     class Meta:
#         model = Appointment
#         fields = '__all__'
        
#         def clean(self):
#             cleaned_data = super().clean()
            
#             doctor = cleaned_data.get('doctor')
#             patient = cleaned_data.get('patient')
#             time = cleaned_data.get('time')
            
#             # Only validate if all 3 fields are present.
#             if doctor and patient and time:
#                 from .validators import validate_appointment
#                 validate_appointment(
#                     doctor=doctor,
#                     patient=patient,
#                     time=time,
#                 )
            
#             return cleaned_data

            
# # -----------------------------
# #  Admin Class
# # -----------------------------
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = ['patient_name', 'doctor_name', 'time', 'appointment_types', 'appointment_status', 'symptom', 'cancel']
    

#     def patient_name(self, obj):
#         return obj.patient.user.first_name

#     def doctor_name(self, obj):
#         return obj.doctor.user.first_name
   
#     # ---- Filter time slots based on selected doctor ----
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "time":
#             doctor_id = (
#                 request.POST.get("doctor")
#                 or request.GET.get("doctor")
#             )
            
#             if doctor_id:
#                 try:
#                     doctor = Doctor.objects.get(id=doctor_id)
#                     kwargs["queryset"] = doctor.available_time.all()
#                 except Doctor.DoesNotExist:
#                     kwargs["queryset"] = Appointment.objects.none()
        
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
#     # ---------------------------------------------
#     # SEND EMAIL WHEN ONLINE APPOINTMENT IS RUNNING
#     # ---------------------------------------------
#     def save_model(self, request, obj, form, change):
#         obj.save()
#         if obj.appointment_status == 'running' and obj.appointment_types == 'online':
#             email_subject = "Your Online Appointment is Running"
#             email_body = render_to_string('appointment/admin_email.html', {'user': obj.patient.user, 'doctor': obj.doctor.user})
            
#             email = EmailMultiAlternatives(email_subject, '', from_email=settings.EMAIL_HOST_USER, to=[obj.patient.user.email])
#             email.attach_alternative(email_body, "text/html")
#             email.send()
            
    
# admin.site.register(Appointment, AppointmentAdmin)


from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Appointment
from doctor.models import Doctor, AvailableTime

class AppointmentAdminForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        
        doctor = cleaned_data.get('doctor')
        patient = cleaned_data.get('patient')
        time = cleaned_data.get('time')
        
        # Only validate if all 3 fields are present
        if doctor and patient and time:
            from .validators import validate_appointment
            try:
                validate_appointment(
                    doctor=doctor,
                    patient=patient,
                    time=time,
                )
            except ValidationError as e:
                # Handle both dictionary errors and string errors
                if hasattr(e, 'message_dict'):
                    # This is a dictionary of field errors
                    for field, messages in e.message_dict.items():
                        for message in messages:
                            self.add_error(field, message)
                else:
                    # This is a non-field error (string)
                    for message in e.messages:
                        self.add_error(None, message)  # None means non-field error
        
        return cleaned_data

class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentAdminForm
    list_display = ['patient_name', 'doctor_name', 'time', 'appointment_types', 'appointment_status', 'symptom', 'cancel']
    
    def patient_name(self, obj):
        if obj.patient and obj.patient.user:
            return obj.patient.user.first_name
        return "No Patient"
    
    def doctor_name(self, obj):
        if obj.doctor and obj.doctor.user:
            return obj.doctor.user.first_name
        return "No Doctor"
    
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
    
    # Send email when online appointment is running
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if (obj.appointment_status == 'running' and 
            obj.appointment_types == 'online' and 
            obj.patient and obj.patient.user and 
            obj.doctor and obj.doctor.user):
            
            try:
                email_subject = "Your Online Appointment is Running"
                email_body = render_to_string(
                    'appointment/admin_email.html', 
                    {'user': obj.patient.user, 'doctor': obj.doctor.user}
                )
                
                email = EmailMultiAlternatives(
                    email_subject, '', 
                    from_email=settings.EMAIL_HOST_USER, 
                    to=[obj.patient.user.email]
                )
                email.attach_alternative(email_body, "text/html")
                email.send()
            except Exception as e:
                print(f"Failed to send email: {e}")

admin.site.register(Appointment, AppointmentAdmin)