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


def get_note(notename, authorname=''):
    note = None
    author = None
    if authorname != 'anonimous':
        author = Author.objects.filter(uid=authorname)
        if not author.exists():
            author = None
        else:
            author = author[0]
    published = Q(name=notename) & Q(published=True)
    if author != None:
        note = Note.objects.filter(
            published | (Q(name=notename) & Q(author=author)))
    else:
        note = Note.objects.filter(published)
    if not note.exists():
        note = None
    return note, author != None


@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def welcome(request):
    return JsonResponse({"message": "ok"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def note_retrieve(request, name):
    payload = loads(dumps(request.data))
    note, ismine = get_note(name, request.session["uid"])
    if ismine and note != None:
        note = note[0]
        serializer = NoteSerializer(note)
        with open(f'sources/{note.name}', 'r') as f:
            return JsonResponse({"message": "retrieved", "note": serializer.data, "source": f.read()}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message": "error", "error": "not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def note_create(request):
    print(request.session["uid"])
    if request.session["uid"] == 'anonimous':
        author = Author(uid=generate_authorname())
        request.session['uid'] = author.uid
        author.save()
        print(author)
    author = Author.objects.get(uid=request.session["uid"])
    note = Note(
        name=generate_notename(),
        author=author,
        language='ace/mode/plain_text',
    )
    note.save()
    with open(f'sources/{note.name}', 'w+') as f:
        f.write('')
    return JsonResponse({"message": "created", "name": note.name}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([AllowAny])
def note_update(request):
    payload = loads(dumps(request.data))
    note, ismine = get_note(payload["name"], request.session["uid"])
    if not ismine or note == None:
        return JsonResponse({"message": "error", "error": "not found"}, status=status.HTTP_404_NOT_FOUND)
    note = note[0]
    allowed_keys = ['language', 'published', 'protected', 'collaborator_link']
    for key in payload.keys():
        if key in allowed_keys:
            setattr(note, key, payload[key])
    if 'source' in payload.keys():
        with open(f'sources/{payload["name"]}', 'w+') as f:
            f.write(f'{payload["source"]}')
    if payload["onclose"]:
        if len(payload["source"]) == 0:
            if path.exists(f'sources/{payload["name"]}'):
                remove(f'sources/{payload["name"]}')
            note.delete()
    return JsonResponse({"message": "updated"}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@csrf_exempt
@permission_classes([AllowAny])
def note_delete(request):
    payload = loads(request.body)
    try:
        note = Note.objects.get(
            name=payload["name"], author=Author.objects.get(uid=payload["author"]))
        if path.exists(f'sources/{payload["name"]}'):
            remove(f'sources/{payload["name"]}')
        note.delete()
        return JsonResponse({"message": "Deleted"}, status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        return JsonResponse({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
