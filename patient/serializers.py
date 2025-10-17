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
        .exclude(doctor__isnull=False,)
    )
    
    class Meta:
        model = Patient
        fields = ['user', 'image', 'mobile_no']
        

# class RegistrationSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField(required=True)
#     class Meta:
#         fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        
#     def save(self):
#         username = self.validated_data['username']
#         email = self.validated_data['email']
#         password = self.validated_data['password']
#         confirm_password = self.validated_data['confirm_password']
        
#         if password != confirm_password:
#             raise serializers.ValidationError({
#                 "error": "Passwords Doesn't Match."
#             })
            
#         if User.objects.filter(email=email).exists():
#             raise serializers.ValidationError({
#                 "error": "Email already exists."
#             })
            
        
#         account = User.objects.create_user(username=username, email=email, password=password) 
#         print(account)
#         account.save()   
#         return account

