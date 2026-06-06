from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token


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


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"},
                                     trim_whitespace=False)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            try:
                user = get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")

            if not user.check_password(password):
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")

            if not user.is_active:
                msg = "User account is disabled."
                raise serializers.ValidationError(msg, code="authorization")

            token, created = Token.objects.get_or_create(user=user)
            data["token"] = token.key
        else:
            msg = "Must include 'email' and 'password'."
            raise serializers.ValidationError(msg, code="authorization")

        return data


