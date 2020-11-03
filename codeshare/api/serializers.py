from rest_framework import serializers
from .models import Author, Note


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['uid']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['language', 'read', 'edit', 'protected']
