"""
Urlpatterns for basket app.

Attributes:
    urlpatterns: List of url paths that are available for basket app.
"""
from django.urls import path

from .views import BasketView

urlpatterns: list[path] = [
    path('basket', BasketView.as_view(), name='basket'),
    path('basket/', BasketView.as_view(), name='basket'),
    ]
