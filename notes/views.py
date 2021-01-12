from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views import View

import json

from . import forms, models

with open('notes/languages.json', 'r') as f:
    LANGUAGES = json.loads(f.read())


def retrieve_note(access_link: str, request_uid: str) -> models.Note:
    author = models.Author.objects.get(uid=request_uid)
    if len(access_link) == 4:
        query = Q(read_link=access_link) & (Q(read=True) | Q(author=author))
    elif len(access_link) == 6:
        query = Q(edit_link=access_link) & (Q(edit=True) | Q(author=author))
    else:
        return None
    note = models.Note.objects.filter(query)
    if note.exists():
        return note[0]
    return None


class LoginView(View):
    context = {'pagename': 'login'}

    def get(self, request):
        self.context['form'] = forms.LoginForm()
        return render(request, 'pages/login.html', self.context)

    def post(self, request):
        form = forms.LoginForm(request.POST)
        self.context['form'] = form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
        return render(request, 'pages/login.html', self.context)


class SignupView(View):
    context = {'pagename': 'signup'}

    def get(self, request):
        self.context['form'] = forms.SignupForm()
        return render(request, 'pages/signup.html', self.context)

    def post(self, request):
        form = forms.SignupForm(request.POST)
        self.context['form'] = form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
        if not form.is_valid():
            self.context['form_errors'] = form.errors
        return render(request, 'pages/signup.html', self.context)


class IndexView(View):
    context = {'pagename': 'index'}

    def get(self, request, access_link=''):
        if 'uid' not in request.session.keys():
            request.session['uid'] = None
        self.context['languages'] = LANGUAGES
        return render(request, 'pages/index.html', self.context)
        

    def post(self, request):
        if 'author' not in request.session.keys():
            author = models.Author()
            author.save()
            request.session['author'] = author.uid
        author = models.Author.objects.get(uid=request.session['author'])
        note = models.Note(author=author)
        if request.POST['language'] is not None:
            note.language = ['plain_text', request.POST['language']][request.POST['language'] in LANGUAGES]
        note.save()
        return JsonResponse({'access_link': note.edit_link})
