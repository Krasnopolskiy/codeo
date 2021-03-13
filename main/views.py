import json
from base64 import b64decode
from urllib.parse import unquote

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django_registration.backends.one_step.views import RegistrationView

from . import misc, models, forms


class ExtendedLoginView(LoginView):
    def post(self, request: HttpRequest, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        if request.user.is_authenticated:
            request.session['author'] = request.user.author.uid
            messages.add_message(request, messages.SUCCESS, 'Logged in')
        else:
            messages.add_message(request, messages.ERROR, 'Error')
        return response


class ExtendedRegistrationView(RegistrationView):
    def post(self, request: HttpRequest, *args, **kwargs):
        response = super(RegistrationView, self).post(request, *args, **kwargs)
        form = forms.SignupForm(request.POST)
        if request.user.is_authenticated:
            request.session['author'] = request.user.author.uid
            messages.add_message(request, messages.SUCCESS, 'Signed up')
        else:
            for error in form.errors.values():
                messages.add_message(request, messages.ERROR, error)
        return response

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
        'init_data': 'null',
        'languages': misc.LANGUAGES
    }

    def get(self, request: HttpRequest, access_link: str = '') -> HttpResponse:
        self.context['pagename'] = 'Editor'
        if 'author' not in request.session:
            author = models.Author()
            author.save()
            request.session['author'] = author.uid
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
            messages.add_message(request, messages.SUCCESS, 'Note deleted')
        return redirect(request.GET.get('next', 'index'))
