"""
Abstract model classes for the Blog project.
"""

from django.db import models


class TimeStampedModel(models.Model):
    """
    Create a model that will keep creation and modification time stamps .
    """

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
