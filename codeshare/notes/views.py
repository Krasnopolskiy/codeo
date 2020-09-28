from django.http import HttpResponse


def index(request):
    return HttpResponse(f'Hello, {request.session}')
