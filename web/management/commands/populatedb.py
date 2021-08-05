"""This specifies a django management command to populate the db with fake data
"""

from django.core.management.base import BaseCommand, CommandError

from commgestion import settings
from web import populate


class Command(BaseCommand):
    help = "Clears existing data and populates the local db with fake data"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError(
                "Not overwriting production data! Not in a debug config!"
            )

        self.stdout.write("Beginning database population...")
        populate.clear_and_add_defaults()
        self.stdout.write(self.style.SUCCESS("Population complete!"))
