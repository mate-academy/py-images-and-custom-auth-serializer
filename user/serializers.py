from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff")  # be careful
        read_only_fields = ("id", "is_staff")  # read-only fields
        extra_kwargs = {  # important fields
            "password": {
                "write_only": True,
                "min_length": 5,
            }
        }

    def create(
        self, validated_data
    ):  # rewriting password creator so it will be encrypted!!!!
        """Create user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(
        self, instance, validated_data
    ):  # rewriting update func specially for password field !!!!!
        """Update user with encrypted password."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email address"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get(
                    "request"
                ),
                email=email,
                password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
