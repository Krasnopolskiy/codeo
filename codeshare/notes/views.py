from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import models


def index(request):
    return HttpResponse('Hello, world')
