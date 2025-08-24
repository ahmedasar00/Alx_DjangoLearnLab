from rest_framework import serializers
from .models import CustomerUserModel
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

UserModel = get_user_model().objects.create_user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUserModel
        fields = [
            "username",
            "email",
            "password",
            "bio",
            "profile_picture",
            "followers",
        ]

    extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}

    def Create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            bio=validated_data("bio"),
            profile_picture=validated_data("profile_picture"),
        )
        Token.object.create(user=user)
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "username", "eamil", "bio", "profile_picture", "followrs"]
