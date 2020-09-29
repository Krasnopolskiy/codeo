from django.db import models


class Author(models.Model):
    uid = models.CharField(max_length=16)
    # uid = "".join(random.choice('0123456789abcdef') for _ in range(16))

    def __str__(self):
        return self.uid


class Note(models.Model):
    name = models.CharField(max_length=4)
    # name = "".join(choice(ascii_letters + digits) for _ in range(4))

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    language = models.CharField(max_length=20)
    collaborator_link = models.CharField(max_length=6, blank=True)
    published = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)

    def __str__(self):
        return self.name
