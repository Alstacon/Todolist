from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import CreateUserSerializer, LoginSerializer, ProfileSerializer, PasswordUpdateSerializer


class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=request.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        login(request=self.request, user=serializer.save())


class ProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        logout(self.request)


class PasswordUpdateView(UpdateAPIView):
    serializer_class = PasswordUpdateSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user
