from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from . import forms, models


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

    def get(self, request, name=''):
        with open('notes/templates/ace_modes.txt', 'r') as f:
            languages = f.read().split('\n')
        self.context['languages'] = languages
        return render(request, 'pages/index.html', self.context)

    def post(self, request):
        return JsonResponse({'user': repr(request.user.__dict__)})
