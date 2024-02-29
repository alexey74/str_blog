"""
Settings for the Blog project.

Mostly boilerplate code here.
This module contains special stanzas to enable Celery.
"""

from .celery_app import app as celery_app

__all__ = ("celery_app",)
