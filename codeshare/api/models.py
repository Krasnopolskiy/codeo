from django.db import models


class Author(models.Model):
    uid = models.CharField(max_length=16)

    '''
    def __init__(self):
        self.uid = "".join(random.choice('0123456789abcdef') for _ in range(16))
    '''

    def __str__(self):
        return self.uid


class Note(models.Model):
    name = models.CharField(max_length=16)
    password_hash = models.CharField(max_length=16, blank=True)
    r_link = models.CharField(max_length=8)
    rw_link = models.CharField(max_length=8)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
