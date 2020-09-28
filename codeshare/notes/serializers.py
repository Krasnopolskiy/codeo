from rest_framework import serializers
from . import models


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Note
        fields = ['url', 'filename', 'r_link', 'rw_link', 'author']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Author
        fields = ['uid']
