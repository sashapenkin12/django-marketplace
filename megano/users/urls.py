"""
A module contains urlpatterns for users app.

Attributes:
    urlpatterns: List of url paths that are available for users app.
"""

from django.urls import path

from .views import SignInView, SignOutView, SignUpView, ProfileView, ChangeAvatarView

urlpatterns: list[path] = [
    path('sign-up', SignUpView.as_view(), name='sign-up'),
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-out', SignOutView.as_view(), name='sign-out'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/avatar', ChangeAvatarView.as_view(), name='change-avatar'),
]