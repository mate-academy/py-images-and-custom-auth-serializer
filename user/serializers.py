from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    "Invalid email or password.", code="authorization"
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    "User account is disabled.", code="authorization"
                )

            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'."
            )

    def create(self, validated_data):
        user = validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key}
