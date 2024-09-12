from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 
            'username',
            'name', 
            'nickname', 
            'email',
            'gender',
        )
        
        
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'nickname',
        )
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'nickname',
            'email',
            'date_joined',
            'birthday',
            'image',
            'gender',
        )