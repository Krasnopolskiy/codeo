from django.db import models
from random import choice


class Author(models.Model):
    uid = models.CharField(max_length=16)

    def __init__(self):
        self.uid = "".join(choice('0123456789abcdef') for _ in range(16))

    def __str__(self):
        return self.uid


class Note(models.Model):
    source_code = models.CharField(max_length=pow(10, 20))
    password_hash = models.CharField(max_length=16)
    r_link = models.CharField(max_length=8)
    rw_link = models.CharField(max_length=8)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.source_code
