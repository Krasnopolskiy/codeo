from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import NoteSerializer, AuthorSerializer
from .models import Note, Author


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def welcome(request):
    content = {"message": "Welcome to the BookStore!"}
    return JsonResponse(content)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def notes(request):
    serializer = NoteSerializer(Note.objects.all(), many=True)
    return JsonResponse({'notes': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def note(request, note_name):
    serializer = NoteSerializer(Note.objects.get(name=note_name))
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@ api_view(["GET"])
@ csrf_exempt
@ permission_classes([IsAuthenticated])
def authors(request):
    serializer = AuthorSerializer(Author.objects.all(), many=True)
    return JsonResponse({'authors': serializer.data}, safe=False, status=status.HTTP_200_OK)
