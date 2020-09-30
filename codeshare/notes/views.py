from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template import loader
from api.models import Note, Author
from api.views import get_note
from django.db.models import Q


def index(request, name=''):
    context = {"source": ""}
    if 'uid' not in request.session.keys():
        request.session["uid"] = "anonimous"
    context["uid"] = request.session["uid"]

    if len(name) != 0:
        note, ismine = get_note(name, request.session["uid"])
        if ismine and note != None:
            with open(f'sources/{name}', 'r') as f:
                context["source"] = f.read()
        if len(context["source"]) == 0:
            return HttpResponseRedirect('/')

    return render(request, 'index.html', context)
