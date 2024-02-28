from django.core.management.base import BaseCommand, CommandError

from blog.mixins.jsonplaceholder import JSONPlaceholderImportMixin, NotEmptyError


class Command(JSONPlaceholderImportMixin, BaseCommand):
    help = """
    Imports data from JSON placeholder API.
    """

    def handle(self, *args, **options):
        try:
            self.import_all()
        except NotEmptyError as err:
            raise CommandError(str(err)) from err
