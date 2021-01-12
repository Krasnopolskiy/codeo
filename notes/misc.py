from django.db.models import Model, Q, query

from string import ascii_letters, digits
from random import choices

from . import models


def generate_unique_field(model: Model, field_name: str, field_size: int) -> str:
    field = ''.join(choices(ascii_letters + digits, k=field_size))
    while model.objects.filter(**{field_name: field}).exists():
        field = ''.join(choices(ascii_letters + digits, k=field_size))
    return field
