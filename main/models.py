from django.db import models
from django.contrib.auth.models import User

import os
from typing import Dict
from datetime import timedelta

from . import misc


class Author(models.Model):
    user = models.OneToOneField(
        User(is_active=False),
        null=True,
        on_delete=models.CASCADE
    )
    uid = models.CharField(max_length=16, null=True)

    def save(self) -> None:
        if not self.pk:
            self.uid = misc.generate_unique_field(Author, 'uid', 16)
        super(Author, self).save()

    def __str__(self) -> str:
        return f'<Author {self.uid}>'


class Note(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    expires = models.DateField(null=True)
    name = models.CharField(max_length=64, default='Untitled')
    language = models.CharField(max_length=20)
    read = models.BooleanField(default=True)
    read_link = models.CharField(max_length=4, null=True)
    edit = models.BooleanField(default=False)
    edit_link = models.CharField(max_length=6, null=True)

    def get_source(self) -> str:
        if os.path.exists(f'sources/{self.read_link}'):
            with open(f'sources/{self.read_link}', 'r') as f:
                return f.read()
        return ''

    def set_source(self, source: str) -> None:
        if misc.validate_base64(source):
            if os.path.exists(f'sources/{self.read_link}'):
                with open(f'sources/{self.read_link}', 'w') as f:
                    f.write(source)

    def set_name(self) -> None:
        self.name = self.name.strip().split('.')[0]
        extension = misc.LANGUAGES[self.language]['extension']
        self.name += extension if extension != '' else ''

    def save(self) -> None:
        if self.pk is None:
            self.read_link = misc.generate_unique_field(Note, 'read_link', 4)
            self.edit_link = misc.generate_unique_field(Note, 'edit_link', 6)
            open(f'sources/{self.read_link}', 'a').close()
        self.language = ['plain_text', self.language][self.language in misc.LANGUAGES]
        self.set_name()
        super(Note, self).save()
        if self.expires is None:
            self.expires = self.created + timedelta(days=1)

    def update(self, access_link: str, request_uid: str, payload: dict) -> None:
        allowed_fields = {'language', 'name'}
        if request_uid == self.author.uid:
            allowed_fields = allowed_fields.union({'read', 'edit'})
        elif access_link != self.edit_link:
            return
        for field in set(payload.keys()) & allowed_fields:
            setattr(self, field, payload[field])
        if 'source' in payload.keys():
            self.set_source(payload['source'])
        self.save()

    def delete(self) -> None:
        if os.path.exists(f'sources/{self.read_link}'):
            os.remove(f'sources/{self.read_link}')
        super(Note, self).delete()

    def serialize(self, request_uid: str) -> Dict:
        context = {
            'editable': {
                'name': self.name,
                'language': self.language,
                'read': self.read,
                'edit': self.edit,
                'source': self.get_source()
            },
            'ismine': False
        }
        if self.author.uid == request_uid:
            context['id'] = self.id
            context['ismine'] = True
            context['read_link'] = self.read_link
            context['edit_link'] = self.edit_link
        return context

    def __str__(self) -> str:
        return f'<Note {self.read_link}>'
