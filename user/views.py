from rest_framework.authtoken.models import Token

from rest_framework import (
    generics,
    authentication,
    permissions,
    authtoken,
    response,
    settings,
)

from user.serializers import UserSerializer, AuthTokenSerializer

from rest_framework.authtoken.views import ObtainAuthToken


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(authtoken.views.ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = settings.api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return response.Response({"token": token.key})


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
