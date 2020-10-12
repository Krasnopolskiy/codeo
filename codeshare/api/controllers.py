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


def generate_collab_link():
    name = "".join(choice(ascii_letters + digits) for _ in range(8))
    while Note.objects.filter(collab_link=name).exists():
        name = "".join(choice(ascii_letters + digits) for _ in range(8))
    return name


def generate_authorname():
    name = "".join(choice(ascii_letters + digits) for _ in range(16))
    while Author.objects.filter(uid=name).exists():
        name = "".join(choice(ascii_letters + digits) for _ in range(16))
    return name


def author_retrieve_or_create(request):
    author = None
    if request.user.is_authenticated:
        author = None
        if 'author' in request.user.keys():
            author = request.user.author
        else:
            author = Author(uid=generate_authorname(), user=request.user)
            request.session['uid'] = author.uid
            author.save()
    if "uid" in request.session.keys() and author == None:
        author = Author.objects.filter(uid=request.session["uid"])
        if not author.exists():
            author = None
        else:
            author = author[0]
    if author == None:
        author = Author(uid=generate_authorname())
        request.session['uid'] = author.uid
        author.save()
    return author, request


def note_create(author):
    note = Note(
        name=generate_notename(),
        author=author,
        language='ace/mode/plain_text',
    )
    note.save()
    with open(f'sources/{note.name}', 'w+') as f:
        f.write('')
    return note


def note_retrieve(notename, session, request):
    note = None
    author = None
    if request.user.is_authenticated:
        author = request.user.author
    if "uid" in session.keys() and author == None:
        author = Author.objects.filter(uid=session["uid"])
        if not author.exists():
            author = None
        else:
            author = author[0]
    if author != None:
        note = Note.objects.filter(Q(name=notename) & Q(author=author))
        if note.exists():
            note = note[0]
        else:
            note = None
            author = None

    if note == None:
        note = Note.objects.filter(Q(name=notename) & Q(published=True))
        author = None
        if note.exists():
            note = note[0]
        else:
            note = None
    return note, author != None, request


def note_update(payload, note):
    allowed_keys = ['language', 'published', 'protected', 'collab_link']
    for key in payload.keys():
        if key in allowed_keys:
            setattr(note, key, payload[key])
    note.save()
    if 'source' in payload.keys():
        with open(f'sources/{note.name}', 'w+') as f:
            f.write(f'{payload["source"]}')
    if "onclose" in payload.keys() and payload["onclose"]:
        if len(payload["source"]) == 0:
            if path.exists(f'sources/{note.name}'):
                remove(f'sources/{note.name}')
            note.delete()


def note_delete(note):
    if path.exists(f'sources/{note.name}'):
        remove(f'sources/{note.name}')
    note.delete()


def note_invite_collaborator(note):
    if len(note.collab_link) == 0:
        link = generate_collab_link()
        note.collab_link = link
        note.save()
