  
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)
    uid = models.CharField(max_length=16)
    def __str__(self):
        return self.uid
class Note(models.Model):
    name = models.CharField(max_length=4)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    language = models.CharField(max_length=20, default ='')
    published = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)
    collaborator_link = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return self.name