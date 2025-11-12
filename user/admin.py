from django.contrib import admin
from .models import Account
from doctor.models import Doctor

from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin): 
    list_display = ('email', 'first_name', 'last_name', 'username', 'date_joined', 'last_login', 'is_active')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
