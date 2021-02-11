from django.core.management.base import BaseCommand
from django.db.models import Count, Q

from main import models


class Command(BaseCommand):
    help = 'Delete authors without notes'

    def handle(self, *args, **options):
        authors = models.Author.objects.annotate(notes_count=Count('note'))
        authors = authors.filter(Q(notes_count=0) & Q(user=None))
        self.stdout.write(self.style.SUCCESS(f'Deleted {len(authors)} authors'))
        [author.delete() for author in authors]
