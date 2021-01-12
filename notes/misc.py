from django.db.models import Model, Q

from string import ascii_letters, digits
from secrets import choice

from . import models


def generate_random_string(size: int) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(size))


def generate_unique_field(model: Model, field_name: str, field_size: int) -> str:
    field = generate_random_string(field_size)
    while model.objects.filter(**{field_name: field}).exists():
        field = generate_random_string(field_size)
    return field


def retrieve_note(access_link: str, request_uid: str) -> Model:
    author = models.Author.objects.get(uid=request_uid)
    if len(access_link) == 4:
        query = Q(read_link=access_link) & (Q(read=True) | Q(author=author))
    elif len(access_link) == 6:
        query = Q(edit_link=access_link) & (Q(edit=True) | Q(author=author))
    else:
        return None
    note = models.Note.objects.filter(query)
    if note.exists():
        return note[0]
    return None