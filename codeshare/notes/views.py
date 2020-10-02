from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template import loader
from api.models import Note, Author


def index(request, name=''):
    if 'uid' not in request.session.keys():
        request.session["uid"] = "anonimous"
    return render(request, 'index.html')
