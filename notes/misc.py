from string import ascii_letters, digits
from random import choices

from . import models


def generate_author_uid():
    uid = ''.join(choices(ascii_letters + digits, k=16))
    while models.Author.objects.filter(uid=uid).exists():
        uid = ''.join(choices(ascii_letters + digits, k=16))
    return uid


def generate_read_link():
    link = ''.join(choices(ascii_letters + digits, k=4))
    while models.Note.objects.filter(read_link=link).exists():
        link = ''.join(choices(ascii_letters + digits, k=4))
    return link


def generate_edit_link():
    link = ''.join(choices(ascii_letters + digits, k=6))
    while models.Note.objects.filter(edit_link=link).exists():
        link = ''.join(choices(ascii_letters + digits, k=6))
    return link