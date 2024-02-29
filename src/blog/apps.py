"""
Django apps module for the Blog project.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Basic app configuration for the Blog project.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
