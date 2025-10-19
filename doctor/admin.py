from django.contrib import admin
from user.models import Account

from . import models

class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    
class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    

    
 
    
admin.site.register(models.Designation, SpecializationAdmin)
admin.site.register(models.Specialization, DesignationAdmin)
admin.site.register(models.AvailableTime)
admin.site.register(models.Doctor)
admin.site.register(models.Review)
