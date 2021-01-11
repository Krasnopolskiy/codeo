from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    uid = models.CharField(max_length=16)

    def __repr__(self):
        return f'<Author {self.uid}>'


class Note(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=True)
    language = models.CharField(max_length=20, default='')

    read = models.BooleanField(default=False)
    read_link = models.CharField(max_length=4)

    edit = models.BooleanField(default=False)
    edit_link = models.CharField(max_length=6, blank=True)

    def __repr__(self):
        return f'<Note {self.read_link}>'
