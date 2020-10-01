from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template import loader
from api.models import Note, Author
from django.db.models import Q


def index(request, name=''):
    context = {"source": ""}
    if 'uid' not in request.session.keys():
        request.session["uid"] = "anonimous"
    context["uid"] = request.session["uid"]

    return render(request, 'index.html', context)
