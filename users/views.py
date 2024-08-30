from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.serializers import UserPublicInfoSerializer, UserSerializer

from .models import User


@extend_schema(
    tags=["Users"],
    summary="Creating a new user",
)
class UserCreateAPIView(CreateAPIView):
    """Creates a new user."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


@extend_schema(
    tags=["Users"],
    summary="Getting a list of all users",
)
class UserListAPIView(ListAPIView):
    """Outputs a list of all users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for user in queryset:
            if request.user == user:
                serializer = self.get_serializer(user)
            else:
                serializer = UserPublicInfoSerializer(user)
            data.append(serializer.data)
        return Response(data)


@extend_schema(
    tags=["Users"],
    summary="Detailed user information",
)
class UserRetrieveAPIView(RetrieveAPIView):
    """Displays detailed information about the user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            serializer = self.get_serializer(instance)
        else:
            serializer = UserPublicInfoSerializer(instance)
        return Response(serializer.data)


@extend_schema(
    tags=["Users"],
    summary="Modifying an existing user",
)
class UserUpdateAPIView(UpdateAPIView):
    """Modifies an existing user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"message": "You cannot edit other user's profile"}, status=403
            )


@extend_schema(
    tags=["Users"],
    summary="Deleting an existing user",
)
class UserDestroyAPIView(DestroyAPIView):
    """Deletes an existing user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "You cannot delete other user's profile"}, status=403
            )

    def perform_destroy(self, instance):
        instance.delete()
