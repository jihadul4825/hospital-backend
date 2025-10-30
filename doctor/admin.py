from django.contrib import admin
from user.models import Account
from django.utils import timezone

from . import models

class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_display = ['id', 'name']
    
class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_display = ['id', 'name']

class DoctorApprovalAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'is_approved', 'approved_at']
    list_filter = ['is_approved']
    list_editable = ['is_approved']
    actions = ['approve_doctors', 'reject_doctors']
    
    def approve_doctors(self, request, queryset):
        # Use update for performance; must set approved_at explicitly because update() bypasses save()
        updated = queryset.update(is_approved=True, approved_at=timezone.now())
        self.message_user(request, f"{updated} doctors approved")

    def reject_doctors(self, request, queryset):
        updated = queryset.update(is_approved=False, approved_at=None)
        self.message_user(request, f"{updated} doctors rejected")
    

class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class DcoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'approval__is_approved','mobile_no', 'fee']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
 

admin.site.register(models.DoctorApproval, DoctorApprovalAdmin)
admin.site.register(models.Designation, SpecializationAdmin)
admin.site.register(models.Specialization, DesignationAdmin)
admin.site.register(models.AvailableTime, AvailableTimeAdmin)
admin.site.register(models.Doctor, DcoctorAdmin)
admin.site.register(models.Review)
