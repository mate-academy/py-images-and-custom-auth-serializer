from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from user.serializers import UserSerializer, CustomAuthTokenSerializer
from django.contrib.auth import get_user_model


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(APIView):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            user = get_user_model()
            try:
                user = user.objects.get(email=email)

                if user.check_password(password):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(
                        {"token": token.key},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "Invalid credentials"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except user.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
