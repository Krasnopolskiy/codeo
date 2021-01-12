from django.db import models
from django.contrib.auth.models import User

from string import ascii_letters, digits
from random import choices


class Author(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    uid = models.CharField(max_length=16, null=True)

    def save(self):
        if not self.pk:
            self.uid = ''.join(choices(ascii_letters + digits, k=16))
            while Author.objects.filter(uid=self.uid).exists():
                self.uid = ''.join(choices(ascii_letters + digits, k=16))
        super(Author, self).save()

    def __repr__(self):
        return f'<Author: {self.uid}>'


class Note(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=True)
    language = models.CharField(max_length=20)

    read = models.BooleanField(default=False)
    read_link = models.CharField(max_length=4, null=True)

    edit = models.BooleanField(default=False)
    edit_link = models.CharField(max_length=6, null=True)

    def save(self):
        if not self.pk:
            self.read_link = ''.join(choices(ascii_letters + digits, k=4))
            while Note.objects.filter(read_link=self.read_link).exists():
                self.read_link = ''.join(choices(ascii_letters + digits, k=4))
            self.edit_link = ''.join(choices(ascii_letters + digits, k=6))
            while Note.objects.filter(edit_link=self.edit_link).exists():
                self.edit_link = ''.join(choices(ascii_letters + digits, k=6))
            open(f'sources/{self.read_link}', 'a').close()
        super(Note, self).save()

    def __repr__(self):
        return f'<Note: {self.read_link}>'
