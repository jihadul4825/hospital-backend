from rest_framework import serializers
from .models import Patient, User



class PatientReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    # first_name = serializers.ReadOnlyField(source='user.first_name')
    # last_name = serializers.ReadOnlyField(source='user.last_name')
    full_name = serializers.ReadOnlyField(source='user.get_full_name')
    
    class Meta:
        model = Patient
        fields = ['id', 'user', 'image', 'mobile_no', 'full_name']


class PatientWriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=False, 
        queryset=User.objects.filter(is_staff=False, is_superuser=False)
        .exclude(doctor__isnull=False)
        .exclude(id__in=Patient.objects.values_list('user', flat=True))
    )
    class Meta:
        model = Patient
        fields = ['user', 'image', 'mobile_no']

