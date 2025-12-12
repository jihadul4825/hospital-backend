import django_filters
from .models import AvailableTime

class AvailableTimeFilter(django_filters.FilterSet):
    doctor_id = django_filters.NumberFilter(field_name="doctor__id")
    class Meta:
        model = AvailableTime
        fields = ['name']