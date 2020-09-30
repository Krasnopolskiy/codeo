from django.shortcuts import render
from django.template import loader
from api.models import Note, Author
from django.db.models import Q
from random import choice
from string import ascii_letters, digits

alpha = ascii_letters + digits


def index(request, name=''):
    context = {'uid': request.session['uid']}
    if name != '':
        note = Note.objects.filter((Q(name=name) & Q(
            author=Author.objects.get(uid=request.session['uid']))) | (Q(name=name) & Q(published=True)))
        if note.exists():
            with open(f'sources/{name}') as f:
                context['source'] = f.read()

    return render(request, 'index.html', context)
