from rest_framework.decorators import api_view
from json import loads
from os import remove, path
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import NoteSerializer, AuthorSerializer
from .models import Note, Author


@api_view(["GET"])
@csrf_exempt
def welcome(request):
    content = {"message": "Welcome to the codeshare api!"}
    return JsonResponse(content, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def note_get(request, name):
    try:
        note = Note.objects.get(name=name, published=True)
        serializer = NoteSerializer(note)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        try:
            payload = loads(request.body)
            author = Author.objects.get(uid=payload["author"])
            note = Note.objects.get(name=name, author=author)
            serializer = NoteSerializer(note)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except:
            return JsonResponse({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@csrf_exempt
def note_create(request):
    payload = loads(request.body)
    author = Author.objects.get(uid=payload["author"])
    Note.objects.create(
        name=payload["name"],
        author=author,
        language=payload["language"],
    )
    with open(f'sources/{payload["name"]}', 'w+') as f:
        f.write(f'{payload["source"]}')
    return JsonResponse({"message": "Created"})


@api_view(["PUT"])
@csrf_exempt
def note_update(request):
    payload = loads(request.body)
    try:
        note = Note.objects.get(
            name=payload["name"], author=Author.objects.get(uid=payload["author"]))
        for el in payload.keys():
            if el != "author" and el != "name":
                setattr(note, el, payload[el])
        note.save()
        if 'source' in payload.keys():
            with open(f'sources/{payload["name"]}', 'w+') as f:
                f.write(f'{payload["source"]}')
        return JsonResponse({"message": "Updated"}, status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        return JsonResponse({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@csrf_exempt
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
