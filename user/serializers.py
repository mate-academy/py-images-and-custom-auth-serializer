from __future__ import annotations

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5}
        }

    def create(
        self, validated_data: dict[str, object]
    ) -> object:
        """Create a new user with encrypted password."""
        return get_user_model().objects.create_user(
            **validated_data
        )

    def update(
        self,
        instance: object,
        validated_data: dict[str, object],
    ) -> object:
        """Update a user, set the password correctly."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)  # type: ignore[union-attr]
            user.save()  # type: ignore[union-attr]
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Auth token serializer using email instead of username."""

    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(
        self, attrs: dict[str, str]
    ) -> dict[str, object]:
        email: str = attrs.get("email", "")
        password: str = attrs.get("password", "")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if not user:
            msg = _(
                "Unable to authenticate with provided credentials."
            )
            raise serializers.ValidationError(
                msg, code="authorization"
            )

        attrs["user"] = user
        return attrs
