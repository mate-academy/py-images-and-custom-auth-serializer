from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
                "label": gettext("Password")
            }
        }

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


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=gettext("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=gettext("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=gettext("Token"),
        read_only=True
    )

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
                msg = gettext(
                    "Unable to authenticate with provided credentials."
                )
                raise serializers.ValidationError(msg, code="authentication")

        else:
            msg = gettext("Must include the email and password.")
            raise serializers.ValidationError(msg, code="authentication")

        attrs["user"] = user
        return attrs
