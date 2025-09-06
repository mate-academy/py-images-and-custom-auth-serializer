from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    AuthTokenSerializer,
    ManageUserSerializer,
)

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args: Any, **kwargs: Any) -> Response:
        serializer = AuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(APIView):
    """POST /api/user/login/  (email+password -> token)"""
    permission_classes = [AllowAny]

    def post(self, request, *args: Any, **kwargs: Any) -> Response:
        s1 = AuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        s1.is_valid(raise_exception=True)
        return Response(s1.validated_data, status=200)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user
