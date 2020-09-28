from rest_framework.decorators import api_view
from json import loads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import NoteSerializer, AuthorSerializer
from .models import Note, Author


@api_view(["GET"])
@csrf_exempt
def welcome(request):
    content = {"message": "Welcome to the codeshare api!"}
    return JsonResponse(content)


@api_view(["GET"])
@csrf_exempt
def note_get(request, note_name):
    serializer = NoteSerializer(Note.objects.get(name=note_name))
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
def note_create(request):
    payload = loads(request.body)
    try:
        author = Author.objects.get(uid=payload["author"])
        note = Note.objects.create(
            name=payload["name"],
            author=author,
            language=payload["language"],
        )
        with open(f'sources/{payload["name"]}', 'w+') as f:
            f.write(f'{payload["source"]}')
        return JsonResponse({"message": "ok"})
    except:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ api_view(["GET"])
@ csrf_exempt
def author_list(request):
    serializer = AuthorSerializer(Author.objects.all(), many=True)
    return JsonResponse({'authors': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def note_list(request):
    serializer = NoteSerializer(Note.objects.all(), many=True)
    return JsonResponse({'notes': serializer.data}, safe=False, status=status.HTTP_200_OK)
