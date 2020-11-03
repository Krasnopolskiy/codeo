
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    uid = models.CharField(max_length=16)

    def __str__(self):
        return self.uid


class Note(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    read = models.BooleanField(default=False)
    name = models.CharField(max_length=4)

    edit = models.BooleanField(default=False)
    edit_link = models.CharField(max_length=6, blank=True)

    language = models.CharField(max_length=20, default='')
    protected = models.BooleanField(default=False)

    def __str__(self):
        return self.name
