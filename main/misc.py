from django.db.models import Model, Q
from django.http.request import HttpRequest

import json
from secrets import choice
from base64 import b64decode
from string import ascii_letters, digits


from . import models


with open('main/static/languages.json', 'r') as f:
    LANGUAGES = json.loads(f.read())


def generate_random_string(size: int) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(size))


def generate_unique_field(model: Model, field_name: str, field_size: int) -> str:
    field = generate_random_string(field_size)
    while model.objects.filter(**{field_name: field}).exists():
        field = generate_random_string(field_size)
    return field


def validate_base64(payload: str) -> bool:
    try:
        b64decode(payload)
        return True
    except:
        return False


def retrieve_note(access_link: str, author: Model) -> Model:
    query = Q(read_link=access_link)
    if len(access_link) == 6:
        query = Q(edit_link=access_link)
    query = query & (Q(read=True) | Q(author__uid=author))
    return models.Note.objects.filter(query).first()


def set_author(request: HttpRequest) -> HttpRequest:
    if 'author' not in request.session:
        author = None
        if request.user.is_authenticated:
            author = models.Author.objects.get(user=request.user)
        if author is None:
            author = models.Author()
            author.save()
        request.session['author'] = author.uid
    return request
