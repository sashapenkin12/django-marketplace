"""
A module contains views for users app requests.
"""
from json import loads
from typing import Any

from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView, Response, Request
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .models import Profile, Image, SiteSetting
from .serializers import ProfileSerializer


class SignUpView(APIView):
    """
    Class-based API view that is needed to register new users

    Methods:
        post(request):
            Send form with new user data to register new user.

    """
    parser_classes = [FormParser]


    def post(self, request: Request) -> Response:
        """
        Handle post requests

        Args:
            request: Current HTTP request with form-data type data.

        Returns:
            Response: The response with 201 status code.
        """
        data: dict = loads(list(request.data.keys())[0])
        username, password, full_name = (
            data.get('username'),
            data.get('password'),
            data.get('name'),
        )
        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            user = authenticate(request, username=username, password=password)
        Profile.objects.create(user=user, fullName=full_name)
        login(request=self.request, user=user)

        return Response(status=status.HTTP_201_CREATED)


class SignInView(APIView):
    """
    Class-based API view that is needed to log in into account.

    Methods:
        post(request):
            Log in into account.

    """
    parser_classes = [FormParser]

    @classmethod
    def post(cls, request: Request) -> Response:
        """
        Handle post requests

        Args:
            request: Current HTTP request with form-data type data.

        Returns:
            Response: The response with 201 status code.

        Raises:
            AuthenticationFailed: If a user with such credentials does not exist.
        """
        data: dict = loads(list(request.data.keys())[0])
        username, password = (
            data.get('username'),
            data.get('password'),
        )
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        raise AuthenticationFailed('Invalid credentials')


class SignOutView(APIView):
    """
    Class-based API view that is needed to log out from account.

    To use this view you need to be authenticated

    Methods:
        post(request):
            Log out from account.

    """
    permission_classes: list[Permission] = [IsAuthenticated]

    @classmethod
    def post(cls, request: Request) -> None:
        """
        Handle post requests

        Args:
            request: Current HTTP request.

        """
        logout(request)


class ProfileView(APIView):
    """
    Class-based API view that works with users profiles.

    To use this view you need to be authenticated

    Methods:
        get(request):
            View current user profile

        post(request):
            Change profile info

    """

    permission_classes: list[Permission] = [IsAuthenticated]

    @classmethod
    def get(cls, request: Request) -> Response:
        """
        Handle get requests

        Args:
            request: Current HTTP request.

        Returns:
            Response: The response with JSON-serialized profile data.
        """
        profile = Profile.objects.select_related('avatar').get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @classmethod
    def post(cls, request: Request) -> Response:
        """
        Handle post requests

        Args:
            request: Current HTTP request with data you would like to change.

        Returns:
            Response: The response with JSON-serialized profile data.
        """
        profile = Profile.objects.select_related('avatar').get(user=request.user)

        profile.fullName = request.data.get('fullName')
        profile.email = request.data.get("email")
        profile.phone = request.data.get('phone')
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ChangeAvatarView(APIView):
    """
    Class-based API view that is needed to change profile avatar.

    To use this view you need to be authenticated

    Methods:
        post(request):
            Change avatar

    """

    parser_classes = [MultiPartParser]
    permission_classes: list[Permission] = [IsAuthenticated]


    @classmethod
    def post(cls, request: Request) -> Response:
        """
        Handle post requests

        Args:
            request: Current HTTP request with image in request.FILES.

        Returns:
            Response: The response with JSON-serialized profile data.
        """
        profile = Profile.objects.select_related('avatar').get(user=request.user)
        avatar, created = Image.objects.get_or_create(
                image=request.FILES['avatar'],
                content=profile.fullName + '_avatar',
            )

        if created:
            if hasattr(profile, 'avatar'):
                profile.avatar.delete()
                profile.save()
            avatar.profile = profile
            avatar.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


def get_setting(key, default=None) -> Any:
    """
    Retrieve site global setting.

    Args:
        key: Name of setting to retrieve.
        default: Default value of setting. Used if the value isn't found in the database.

    Returns:
        Any: Setting value.
    """
    cached_value = cache.get(f'{key}')
    if cached_value is not None:
        return cached_value

    try:
        setting = SiteSetting.objects.get(key=key)
        cache.set(f'site_setting_{key}', setting.value, timeout=3600)
        return setting.value
    except SiteSetting.DoesNotExist:
        return default
