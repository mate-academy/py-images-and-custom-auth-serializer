from django.contrib.auth import authenticate
from rest_framework import serializers


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                username=email, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials.",
                    code="authorization",
                )
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".',
                code="authorization",
            )
        attrs["user"] = user
        return attrs
