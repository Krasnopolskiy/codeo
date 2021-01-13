from django.contrib.auth import login, authenticate
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.urls import reverse
from django.views import View

from . import forms, models, misc


class LoginView(View):
    context = {'pagename': 'login'}

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
                author = models.Author.objects.filter(user=user)
                if not author.exists():
                    author = models.Author(user=user)
                    author.save()
                else:
                    author = author[0]
                request.session['author'] = author.uid
                return redirect(reverse('index'))
        return render(request, 'pages/login.html', self.context)


class SignupView(View):
    context = {'pagename': 'signup'}

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


class IndexView(View):
    context = {'pagename': 'index'}

    def get(self, request: HttpRequest, access_link: str='') -> HttpResponse:
        if 'author' not in request.session.keys():
            author = models.Author()
            author.save()
            request.session['author'] = author.uid
        self.context['languages'] = misc.LANGUAGES
        return render(request, 'pages/index.html', self.context)

    def post(self, request: HttpRequest) -> JsonResponse:
        if 'author' not in request.session.keys():
            author = models.Author()
            author.save()
            request.session['author'] = author.uid
        author = models.Author.objects.get(uid=request.session['author'])
        note = models.Note(author=author)
        if request.POST['language'] is not None:
            note.language = ['plain_text', request.POST['language']][request.POST['language'] in misc.LANGUAGES]
        note.save()
        return JsonResponse({
            'read_link': note.read_link,
            'edit_link': note.edit_link
        })


class DashboardView(View):
    context = {'pagename': 'dashboard'}

    def get(self, request: HttpRequest) -> HttpResponse:
        author = models.Author.objects.get(user=request.user)
        notes = models.Note.objects.filter(author=author)
        self.context['notes'] = notes
        return render(request, 'pages/dashboard.html', self.context)