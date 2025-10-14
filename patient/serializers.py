from rest_framework import serializers
from .models import Patient
class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    # first_name = serializers.ReadOnlyField(source='user.first_name')
    # last_name = serializers.ReadOnlyField(source='user.last_name')
    full_name = serializers.ReadOnlyField(source='user.get_full_name')
    
    class Meta:
        model = Patient
        fields = ['id', 'user', 'image', 'mobile_no', 'full_name']