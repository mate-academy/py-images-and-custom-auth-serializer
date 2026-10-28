from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer, UserRegisterSerializer
from .auth import EmailAuthTokenSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailAuthTokenSerializer


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
