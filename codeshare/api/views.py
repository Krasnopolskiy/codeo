from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
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


@api_view(["GET"])
@csrf_exempt
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def welcome(request):
    content = {"message": "Welcome to the codeshare api!"}
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def note_create(request):
    payload = loads(dumps(request.data))
    name = generate_notename()
    if 'uid' not in request.session.keys():
        name = generate_authorname()
        request.session['uid'] = name
        author = Author(uid=name)
        author.save()
    author = Author.objects.get(uid=request.session["uid"])
    Note.objects.create(
        name=name,
        author=author,
        language=payload["language"],
    )
    with open(f'sources/{name}', 'w+') as f:
        f.write(f'{payload["source"]}')
    return JsonResponse({"message": "Created", "name": name})


@api_view(["PUT"])
@csrf_exempt
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def note_update(request):
    payload = loads(dumps(request.data))
    print(payload)
    note = Note.objects.filter(Q(name=payload["name"]) | Q(
        author=Author.objects.get(uid=request.session["uid"])))

    if not note.exists():
        return JsonResponse({"message": "Not Found"})

    note = note[0]
    for key in payload.keys():
        if key in ['language', 'published', 'protected', 'collaborator_link']:
            setattr(note, key, payload[key])

    if 'source' in payload.keys():
        with open(f'sources/{payload["name"]}', 'w+') as f:
            f.write(f'{payload["source"]}')

    if payload["onclose"]:
        if len(payload["source"]) == 0:
            if path.exists(f'sources/{payload["name"]}'):
                remove(f'sources/{payload["name"]}')
            note.delete()

    return JsonResponse({"message": "Updated", "name": payload["name"]})


@api_view(["DELETE"])
@csrf_exempt
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
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


@api_view(["GET"])
@csrf_exempt
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def note_list(request):
    try:
        payload = loads(request.body)
        author = Author.objects.get(uid=payload["author"])
        notes = Note.objects.filter(Q(published=True) | Q(
            author=author))
    except:
        notes = Note.objects.filter(published=True)
    serializer = NoteSerializer(notes, many=True)
    return JsonResponse({'notes': serializer.data}, safe=False, status=status.HTTP_200_OK)
