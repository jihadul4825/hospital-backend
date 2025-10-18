from rest_framework import serializers
from .models import Account
from django.db import transaction


class AccountSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']

    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "error": "Passwords Doesn't Match."
            })
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
        validated_data.pop('confirm_password')
        return Account.objects.create_user(**validated_data)


