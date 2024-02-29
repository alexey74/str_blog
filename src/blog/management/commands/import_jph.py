"""
Management command module for importing data.
"""

from typing import Any

from django.core.management.base import BaseCommand, CommandError

from blog.mixins.jsonplaceholder import JSONPlaceholderImportMixin, NotEmptyError


class Command(JSONPlaceholderImportMixin, BaseCommand):
    """
    Management command class for importing data.

    Imports all data from JSON placeholder API into local DB.

    Raises:
        CommandError: if DB tables not empty
    """

    help = """
    Imports data from JSON placeholder API.
    """

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            self.import_all()
        except NotEmptyError as err:
            raise CommandError(str(err)) from err
