from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from json import loads, dumps
from .serializers import NoteSerializer
from .controllers import *
from django.contrib.auth.models import User


@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_create(request):
    payload = loads(dumps(request.data))

    author = author_retrieve(request)
    if not author:
        author, request = author_create(request)

    note = note_create(author)
    note_update(note, author, payload)
    return JsonResponse({'message': 'created', 'name': note.name, 'edit_link': note.edit_link}, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_retrieve(request, name):
    note = note_retrieve(name)
    if not note:
        return JsonResponse({'message': 'error', 'event': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    author = author_retrieve(request)
    if not author:
        author, request = author_create(request)
    ismine = note.author == author

    if not note.read:
        if note.author != author:
            return JsonResponse({'message': 'error', 'event': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

    with open(f'sources/{note.name}', 'r') as f:
        serializer = NoteSerializer(note)
        context = {'message': 'retrieved', 'note': serializer.data,
                   'source': f.read(), 'ismine': ismine}
        context["edit_link"] = [
            None, note.edit_link][ismine or name == note.edit_link]
        return JsonResponse(context, status=status.HTTP_200_OK)
