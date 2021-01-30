from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse
from django.views import View

import json
from base64 import b64decode

from . import forms, models, misc


class LoginView(View):
    context = {'pagename': 'Login'}

    def get(self, request: HttpRequest) -> HttpResponse:
        self.context['form'] = forms.LoginForm()
        return render(request, 'pages/login.html', self.context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = forms.LoginForm(request.POST)
        self.context['form'] = form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                author = models.Author.objects.filter(user=user).first()
                if author is None:
                    author = models.Author(user=user)
                    author.save()
                request.session['author'] = author.uid
                return redirect(reverse('dashboard'))
        return render(request, 'pages/login.html', self.context)


class SignupView(View):
    context = {'pagename': 'Signup'}

    def get(self, request: HttpRequest) -> HttpResponse:
        self.context['form'] = forms.SignupForm()
        return render(request, 'pages/signup.html', self.context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = forms.SignupForm(request.POST)
        self.context['form'] = form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                return redirect(reverse('login'))
        if not form.is_valid():
            self.context['form_errors'] = form.errors
        return render(request, 'pages/signup.html', self.context)


class RetrieveNoteView(View):
    context = {'pagename': 'Retreive note'}

    def get(self, request: HttpRequest, access_link: str) -> HttpResponse:
        if 'author' not in request.session.keys():
            return redirect(reverse('index'))
        note = misc.retrieve_note(access_link, request.session['author'])
        source = b64decode(note.get_source().encode()).decode()
        return HttpResponse(source, content_type="text/plain")

class IndexView(View):
    context = {'pagename': 'Editor'}

    def get(self, request: HttpRequest, access_link: str = '') -> HttpResponse:
        if 'author' not in request.session.keys():
            author = models.Author()
            author.save()
            request.session['author'] = author.uid
        self.context['languages'] = misc.LANGUAGES
        self.context['init_data'] = 'undefined'
        note = misc.retrieve_note(access_link, request.session['author'])
        if note is not None:
            self.context['init_data'] = json.dumps(note.serialize(request.session['author']))
            self.context['pagename'] = note.name
        return render(request, 'pages/index.html', self.context)

    def post(self, request: HttpRequest) -> JsonResponse:
        author = models.Author.objects.filter(uid=request.session['author']).first()
        note = models.Note(author=author, language=request.POST.get('language'))
        note.save()
        return JsonResponse({'init_data': note.serialize(request.session['author'])})


class DashboardView(LoginRequiredMixin, View):
    context = {'pagename': 'Dashboard'}

    def get(self, request: HttpRequest) -> HttpResponse:
        author = models.Author.objects.filter(user=request.user).first()
        notes = models.Note.objects.filter(author=author)
        self.context['notes'] = notes
        self.context['host'] = request.build_absolute_uri().split('/')[2] + '/'
        self.context['languages'] = misc.LANGUAGES
        return render(request, 'pages/dashboard.html', self.context)


class DeleteNoteView(View):
    context = {'pagename': 'Delete note'}

    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        note = models.Note.objects.filter(id=id).first()
        if note is not None and request.session['author'] == note.author.uid:
            note.delete()
        return redirect(request.GET.get('next', 'index'))