from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse
from django.views import View

import json
from base64 import b64decode
from urllib.parse import unquote

from . import models, misc


class DashboardView(LoginRequiredMixin, View):
    context = {'pagename': 'Dashboard'}

    def get(self, request: HttpRequest) -> HttpResponse:
        author = models.Author.objects.filter(user=request.user).first()
        notes = models.Note.objects.filter(author=author)
        self.context['notes'] = notes
        self.context['host'] = request.build_absolute_uri().split('/')[2] + '/'
        self.context['languages'] = misc.LANGUAGES
        return render(request, 'pages/dashboard.html', self.context)


class EditorView(View):
    context = {
        'pagename': 'Editor',
        'init_data': 'null',
        'languages': misc.LANGUAGES
    }

    def get(self, request: HttpRequest, access_link: str = '') -> HttpResponse:
        self.context['pagename'] = 'Editor'
        request = misc.set_author(request)
        note = misc.retrieve_note(access_link, request.session['author'])
        if note is not None:
            self.context['init_data'] = json.dumps(note.serialize(request.session['author']))
            self.context['pagename'] = note.name
        return render(request, 'pages/editor.html', self.context)

    def post(self, request: HttpRequest) -> JsonResponse:
        author = models.Author.objects.filter(uid=request.session['author']).first()
        note = models.Note(
            author=author,
            name=request.POST.get('name', 'Untitled'),
            language=request.POST.get('language', 'plain_text')
        )
        note.save()
        note.set_source(request.POST.get('source', ''))
        return JsonResponse({'init_data': note.serialize(request.session['author'])})


class RawView(View):
    context = {'pagename': 'Raw'}

    def get(self, request: HttpRequest, access_link: str) -> HttpResponse:
        if 'author' not in request.session.keys():
            return redirect(reverse('index'))
        note = misc.retrieve_note(access_link, request.session['author'])
        source = unquote(b64decode(note.get_source().encode()))
        return HttpResponse(source, content_type='text/plain')


class DeleteView(View):
    context = {'pagename': 'Delete'}

    def get(self, request: HttpRequest, access_link: str) -> HttpResponse:
        note = misc.retrieve_note(access_link, request.session['author'])
        if note is not None and request.session['author'] == note.author.uid:
            note.delete()
        return redirect(request.GET.get('next', 'index'))
