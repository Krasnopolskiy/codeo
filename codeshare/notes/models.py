from django.db import models
from random import choice


class Author(models.Model):
    uid = models.CharField(max_length=16)

    '''
    def __init__(self):
        self.uid = "".join(choice('0123456789abcdef') for _ in range(16))
    '''

    def __unicode__(self):
        return self.uid


class Note(models.Model):
    filename = models.CharField(max_length=16)
    password_hash = models.CharField(max_length=16)
    r_link = models.CharField(max_length=8)
    rw_link = models.CharField(max_length=8)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
