from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "is_staff",
        )
        read_only_fields = (
            "id",
            "is_staff",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            **validated_data,
        )

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        user = super().update(
            instance,
            validated_data,
        )

        if password:
            user.set_password(password)
            user.save(update_fields=["password"])

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            email=attrs.get("email"),
            password=attrs.get("password"),
        )

        if not user:
            raise serializers.ValidationError(
                _(
                    "Unable to authenticate with provided credentials."
                ),
                code="authorization",
            )

        attrs["user"] = user

        return attrs
