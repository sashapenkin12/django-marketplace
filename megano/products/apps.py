"""
Products app config module
"""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Config of the products' app.

    Attributes:
        default_auto_field: A field that automatically increases when an object is added.
        name: Name of the app.
        verbose_name: Representing name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    verbose_name = 'Товары'
