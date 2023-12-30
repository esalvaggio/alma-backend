from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
          model = User
          fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'password']
          extra_kwargs = {
            'last_name': {'required': False},
            'email': {'required': False},
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name',''),
            email=validated_data.get('email',''),
            password=validated_data.get('password'),
        )
        return user