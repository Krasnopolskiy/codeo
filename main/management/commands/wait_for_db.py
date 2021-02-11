from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand

from time import sleep

class Command(BaseCommand):
    help = 'Django command to pause execution until db is available'

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waititng 1 second...')
                sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))