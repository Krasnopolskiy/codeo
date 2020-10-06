from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from json import loads, dumps
from .serializers import NoteSerializer
from .controllers import *


@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def api_welcome(request):
    return JsonResponse({"message": "Api is working"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_retrieve(request, name):
    note, ismine = note_retrieve(name, request.session)
    if note != None:
        serializer = NoteSerializer(note)
        with open(f'sources/{note.name}', 'r') as f:
            context = {"message": "retrieved", "note": serializer.data,
                       "source": f.read(), "ismine": ismine}
            if ismine:
                context["collaborator_link"] = note.collaborator_link
            return JsonResponse(context, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message": "error", "event": "not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_create(request):
    payload = loads(dumps(request.data))
    author, request = author_retrieve_or_create(request)
    note = note_create(author)
    note_update(payload, note)
    return JsonResponse({"message": "created", "notename": note.name}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_update(request):
    payload = loads(dumps(request.data))
    note, ismine = note_retrieve(payload["name"], request.session)
    if note == None:
        return JsonResponse({"message": "error", "event": "not found"}, status=status.HTTP_404_NOT_FOUND)
    if not ismine:
        return JsonResponse({"message": "error", "event": "forbidden"}, status=status.HTTP_403_FORBIDDEN)
    note_update(payload, note)
    return JsonResponse({"message": "updated"}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_delete(request):
    payload = loads(dumps(request.data))
    note, ismine = note_retrieve(payload["name"], request.session)
    if note == None:
        return JsonResponse({"message": "error", "event": "not found"}, status=status.HTTP_404_NOT_FOUND)
    if not ismine:
        return JsonResponse({"message": "error", "event": "forbidden"}, status=status.HTTP_403_FORBIDDEN)
    note_delete(note)
    return JsonResponse({"message": "deleted"}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([AllowAny])
def api_note_invite_collaborator(request):
    payload = loads(dumps(request.data))
    note, ismine = note_retrieve(payload["name"], request.session)
    if note == None:
        return JsonResponse({"message": "error", "event": "not found"}, status=status.HTTP_404_NOT_FOUND)
    if not ismine:
        return JsonResponse({"message": "error", "event": "forbidden"}, status=status.HTTP_403_FORBIDDEN)
    note_invite_collaborator(note)
    return JsonResponse({"message": "invited", "link": note.collab_link},
                        status=status.HTTP_200_OK)
