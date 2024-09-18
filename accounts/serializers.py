from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "password",
            "username",
            "email",
            "name",
            "nickname",
            "birthday",
            "gender",
            "introduction",
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
        
        
class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'nickname',
            'email',
            'birthday',
            'image',
            'gender',
            'introduction',
        )

