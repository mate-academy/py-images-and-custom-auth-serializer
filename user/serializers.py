from django.contrib.auth import get_user_model
from rest_framework import serializers

from django.utils.translation import gettext as _


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
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # Attempt to authenticate the user
            user = get_user_model().objects.filter(email=email).first()

            if user:
                # Check if the user's password is valid
                if user.check_password(password):
                    if not user.is_active:
                        msg = _("User account is disabled.")
                        raise serializers.ValidationError(msg)

                    attrs["user"] = user
                    return attrs
                else:
                    msg = _("Invalid password.")
                    raise serializers.ValidationError(msg)
            else:
                msg = _("No user with this email address.")
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg)
