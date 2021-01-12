from django.db.models import Model

from string import ascii_letters, digits
from secrets import choice


def generate_random_string(size: int) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(size))


def generate_unique_field(model: Model, field_name: str, field_size: int) -> str:
    field = generate_random_string(field_size)
    while model.objects.filter(**{field_name: field}).exists():
        field = generate_random_string(field_size)
    return field
