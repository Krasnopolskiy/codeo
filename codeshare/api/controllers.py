from random import choice
from .models import Note, Author
from string import ascii_letters, digits
from os import remove, path
from django.db.models import Q
from django.contrib.auth.models import User


def generate_notename():
    name = "".join(choice(ascii_letters + digits) for _ in range(4))
    while Note.objects.filter(name=name).exists():
        name = "".join(choice(ascii_letters + digits) for _ in range(4))
    return name


def generate_edit_link():
    name = "".join(choice(ascii_letters + digits) for _ in range(6))
    while Note.objects.filter(edit_link=name).exists():
        name = "".join(choice(ascii_letters + digits) for _ in range(6))
    return name


def generate_authorname():
    name = "".join(choice(ascii_letters + digits) for _ in range(16))
    while Author.objects.filter(uid=name).exists():
        name = "".join(choice(ascii_letters + digits) for _ in range(16))
    return name


def author_create(request):
    author = Author(uid=generate_authorname())
    request.session['uid'] = author.uid
    author.save()
    return author, request


def author_retrieve(request):
    author = None
    if request.user.is_authenticated:
        try:
            author = request.user.author
        except:
            pass
    if "uid" in request.session.keys() and author == None:
        author = Author.objects.filter(uid=request.session["uid"])
        if author.exists():
            author = author[0]
        else:
            author = None
    return author


def note_create(author):
    note = Note(
        name=generate_notename(),
        edit_link=generate_edit_link(),
        author=author,
        language='ace/mode/plain_text',
    )
    note.save()
    with open(f'sources/{note.name}', 'w+') as f:
        f.write('')
    return note


def note_retrieve(name):
    note = Note.objects.filter(Q(name=name) | (
        Q(edit_link=name) & Q(edit=True)))
    if not note.exists():
        return None
    return note[0]


def note_update(note, author, payload):
    if 'language' in payload.keys():
        note.language = payload["language"]
    if 'source' in payload.keys():
        with open(f'sources/{note.name}', 'w+') as f:
            f.write(f'{payload["source"]}')
    if author == note.author:
        settings = ['read', 'edit']
        for key in payload.keys():
            if key in settings:
                setattr(note, key, payload[key])
        if 'onclose' in payload.keys() and payload["onclose"]:
            if len(payload["source"]) == 0:
                note_delete(note)
    note.save()


def note_delete(note):
    if path.exists(f'sources/{note.name}'):
        remove(f'sources/{note.name}')
    note.delete()
