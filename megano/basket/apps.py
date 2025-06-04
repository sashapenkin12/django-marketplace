"""
Basket app config module
"""

from django.apps import AppConfig


class BasketConfig(AppConfig):
    """
    Config of the basket app.

    Attributes:
        default_auto_field: A field that automatically increases when an object is added.
        name: Name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basket'
