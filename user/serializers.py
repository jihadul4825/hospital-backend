from rest_framework import serializers
from .models import Account
from django.db import transaction


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
        

    def validate_password_policy(self, password):
        if not password:
            raise serializers.ValidationError("Password is required.")
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if password.isdigit():
            raise serializers.ValidationError("Password cannot be only numbers.")
        # Optional stronger rule: require at least one letter and one digit
        # if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
        #     raise serializers.ValidationError("Password must contain at least one letter and one number.")
        return password
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "error": "Passwords Doesn't Match."
            })
        self.validate_password_policy(data['password'])
        return data
    
    def validate_email(self, email):
        if Account.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "error": "Email already exists."
            })
        return email
    
    def validate_username(self, username):
        if Account.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "error": "Username already exists."
            })
        return username
    
    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return Account.objects.create_user(**validated_data)
    
    
    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)
        if password:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


