""" Explains all the apps that should be called by catalog"""

from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Configuration class for the catalog application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
