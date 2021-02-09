from django.core.management.base import BaseCommand

from datetime import datetime

from main import models

class Command(BaseCommand):
    help = 'Delete expired and empty notes'

    def handle(self, *args, **options):
        notes = models.Note.objects.filter(expires__lt=datetime.now())
        self.stdout.write(f'Deleted {len(notes)} notes')
        [note.delete() for note in notes]
