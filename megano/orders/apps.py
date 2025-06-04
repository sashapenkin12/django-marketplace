"""
Orders app config module
"""
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Config of the orders' app.

    Attributes:
        default_auto_field: A field that automatically increases when an object is added.
        name: Name of the app.
        verbose_name: Representing name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    verbose_name = 'Заказы'
