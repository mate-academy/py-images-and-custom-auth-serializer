from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=False, min_length=5
    )

    class Meta:
        model = User
        fields = ("id", "email", "is_staff", "password")
        read_only_fields = ("id", "is_staff")

    def update(self, instance, validated):
        pwd = validated.pop("password", None)
        user = super().update(instance, validated)
        if pwd:
            user.set_password(pwd)
            user.save(update_fields=["password"])
        return user


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
