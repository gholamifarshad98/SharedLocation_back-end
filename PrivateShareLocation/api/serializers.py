# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserLocation, SharedUser, AllowedUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'email': {'required': False}}  # Email optional for compatibility

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),  # Default to empty string if not provided
            password=validated_data['password']
        )
        return user

class UserLocationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserLocation
        fields = ['id', 'user', 'latitude', 'longitude', 'last_updated']

class SharedUserSerializer(serializers.ModelSerializer):
    shared_with = UserSerializer(read_only=True)
    last_update = serializers.SerializerMethodField()

    class Meta:
        model = SharedUser
        fields = ['id', 'shared_with', 'last_viewed', 'last_update']

    def get_last_update(self, obj):
        latest_location = UserLocation.objects.filter(user=obj.shared_with).order_by('-last_updated').first()
        return latest_location.last_updated if latest_location else None

class AllowedUserSerializer(serializers.ModelSerializer):
    allowed_to = UserSerializer(read_only=True)

    class Meta:
        model = AllowedUser
        fields = ['id', 'allowed_to', 'last_viewed']