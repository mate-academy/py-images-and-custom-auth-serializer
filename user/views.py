
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
