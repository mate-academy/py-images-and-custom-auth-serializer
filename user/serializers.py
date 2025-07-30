from django.contrib.auth import get_user_model
from rest_framework import serializers
from cinema.models import Movie
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["image"]

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                username=email,  # username = email, т.к. ты используешь email как логин
                password=password
            )
            if not user:
                raise serializers.ValidationError(
                    _("Unable to authenticate with provided credentials"),
                    code="authorization"
                )
        else:
            raise serializers.ValidationError(
                _("Must include 'email' and 'password'."),
                code="authorization"
            )

        attrs["user"] = user
        return attrs
