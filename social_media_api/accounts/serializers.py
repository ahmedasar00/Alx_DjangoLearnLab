from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()
# object.create_user()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "email",
            "password",
            "bio",
            "profile_picture",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            bio=validated_data.get("bio", ""),
            profile_picture=validated_data.get("profile_picture", None),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "profile_picture",
            "followers",
            "following",
        ]
