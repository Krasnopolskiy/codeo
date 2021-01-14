from django.contrib import admin

from notes import models

admin.site.register(models.Author, models.Note)