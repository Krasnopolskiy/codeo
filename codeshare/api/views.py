from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from json import loads, dumps
from os import remove, path
from random import choice
from string import ascii_letters, digits
from .serializers import NoteSerializer, AuthorSerializer
from .models import Note, Author


def generate_notename():
    name = "".join(choice(ascii_letters + digits) for _ in range(4))
    while Note.objects.filter(name=name).exists():
        name = "".join(choice(ascii_letters + digits) for _ in range(4))
    return name


def generate_authorname():
    name = "".join(choice(ascii_letters + digits) for _ in range(16))
    while Author.objects.filter(uid=name).exists():
        name = "".join(choice(ascii_letters + digits) for _ in range(16))
    return name


def note_retrieve(notename, authorname='anonimous'):
    note = None
    author = None

    if authorname != 'anonimous':
        author = Author.objects.filter(uid=authorname)
        if not author.exists():
            author = None
        else:
            author = author[0]
    if author != None:
        note = Note.objects.filter(Q(name=notename) & Q(author=author))
        if note.exists():
            note = note[0]
        else:
            note = None
            author = None

    if note == None:
        note = Note.objects.filter(Q(name=notename) & Q(published=True))
        author = None
        if note.exists():
            note = note[0]
        else:
            note = None

    return note, author != None


def note_update(payload, note):

    allowed_keys = ['language', 'published', 'protected', 'collaborator_link']
    for key in payload.keys():
        if key in allowed_keys:
            setattr(note, key, payload[key])
    note.save()
    if 'source' in payload.keys():
        with open(f'sources/{note.name}', 'w+') as f:
            f.write(f'{payload["source"]}')
    if "onclose" in payload.keys() and payload["onclose"]:
        if len(payload["source"]) == 0:
            if path.exists(f'sources/{note.name}'):
                remove(f'sources/{note.name}')
            note.delete()


@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def api_welcome(request):
    return JsonResponse({"message": "Api is working"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_retrieve(request, name):
    note, ismine = note_retrieve(name, request.session["uid"])
    if note != None:
        serializer = NoteSerializer(note)
        with open(f'sources/{note.name}', 'r') as f:
            return JsonResponse({"message": "retrieved", "note": serializer.data, "source": f.read(), "ismine": ismine}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message": "error", "event": "not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_create(request):
    payload = loads(dumps(request.data))
    if request.session["uid"] == 'anonimous':
        author = Author(uid=generate_authorname())
        request.session['uid'] = author.uid
        author.save()
    author = Author.objects.get(uid=request.session["uid"])
    note = Note(
        name=generate_notename(),
        author=author,
        language='ace/mode/plain_text',
    )
    note.save()
    with open(f'sources/{note.name}', 'w+') as f:
        f.write('')
    note_update(payload, note)
    return JsonResponse({"message": "created", "notename": note.name}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_update(request):
    payload = loads(dumps(request.data))
    note, ismine = note_retrieve(payload["name"], request.session["uid"])
    if note == None:
        return JsonResponse({"message": "error", "event": "not found"}, status=status.HTTP_404_NOT_FOUND)
    if not ismine:
        return JsonResponse({"message": "error", "event": "you cannot edit this note"}, status=status.HTTP_403_FORBIDDEN)
    note_update(payload, note)
    return JsonResponse({"message": "updated"}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_delete(request):
    payload = loads(dumps(request.data))
    note, ismine = note_retrieve(payload["name"], request.session["uid"])
    if note == None or not ismine:
        return JsonResponse({"message": "error", "event": "not found"}, status=status.HTTP_404_NOT_FOUND)
    if path.exists(f'sources/{note.name}'):
        remove(f'sources/{note.name}')
    note.delete()
    return JsonResponse({"message": "deleted"}, status=status.HTTP_200_OK)
