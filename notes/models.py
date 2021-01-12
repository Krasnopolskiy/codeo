import json
from typing import Dict
from django.db import models
from django.contrib.auth.models import User

from . import misc


class Author(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    uid = models.CharField(max_length=16, null=True)

    def save(self) -> None:
        if not self.pk:
            self.uid = misc.generate_unique_field(Author, 'uid', 16)
        super(Author, self).save()

    def __repr__(self) -> str:
        return f'<Author: {self.uid}>'


class Note(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=True)
    language = models.CharField(max_length=20)

    read = models.BooleanField(default=False)
    read_link = models.CharField(max_length=4, null=True)

    edit = models.BooleanField(default=False)
    edit_link = models.CharField(max_length=6, null=True)

    def save(self) -> None:
        if not self.pk:
            self.read_link = misc.generate_unique_field(Note, 'read_link', 4)
            self.edit_link = misc.generate_unique_field(Note, 'edit_link', 6)
            open(f'sources/{self.read_link}', 'a').close()
        super(Note, self).save()

    def get_source(self) -> str:
        with open(f'sources/{self.read_link}', 'r') as f:
            return f.read()

    def set_source(self, source) -> None:
        with open(f'sources/{self.read_link}', 'w') as f:
            f.write(source)
    
    def serialize(self, request_uid: str) -> str:
        context = {
            'ismine': False,
            'language': self.language,
            'source': self.get_source(),
        }
        if self.author.uid == request_uid:
            context['ismine'] = True
            context['read'] = self.read
            context['read_link'] = self.read_link
            context['edit'] = self.edit
            context['edit_link'] = self.edit_link
        return json.dumps(context)

    def __repr__(self) -> str:
        return f'<Note: {self.read_link}>'
