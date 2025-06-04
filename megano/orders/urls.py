"""
Module with urlpatterns for orders app.

Attributes:
    urlpatterns: List of url paths that are available for orders app.
"""
from django.urls import path

from .views import OrdersView, GetConfirmOrderView, PaymentView

urlpatterns: list[path] = [
    path('orders', OrdersView.as_view(), name='orders'),
    path('order/<int:pk>', GetConfirmOrderView.as_view(), name='get-confirm-order'),
    path('payment/<int:pk>', PaymentView.as_view(), name='payment')
]
