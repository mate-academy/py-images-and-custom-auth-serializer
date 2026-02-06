from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer para o objeto de usuário."""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Cria e retorna um usuário com senha criptografada."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Atualiza o usuário, configurando a senha corretamente e retorna-o."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer para o token de autenticação do usuário."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Valida e autentica o usuário."""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email, # O Django usa 'username' como parâmetro, mas passamos o email
            password=password,
        )

        if not user:
            msg = _("Incapaz de autenticar com as credenciais fornecidas.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
