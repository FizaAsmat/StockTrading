from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email','password')

    def create(self, validated_data):
        user = User(
            username=validated_data('username'),
            email=validated_data('email'),
        )
        user.set_password(validated_data['password'])
        user.is_staff=False
        user.save()
        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_staff:  # ✅ only non-admin users
            data['username'] = self.user.username
            data['email'] = self.user.email
            data['role'] = 'user'
            return data
        else:
            raise serializers.ValidationError("Admin cannot login from this endpoint.")


class AdminLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.is_staff:  # ✅ only admin users
            data['username'] = self.user.username
            data['email'] = self.user.email
            data['role'] = 'admin'
            return data
        else:
            raise serializers.ValidationError("Only admins can login from this endpoint.")
