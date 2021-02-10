from django.contrib.auth import login, authenticate
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse
from django.views import View

from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token
from django.contrib.auth.models import User


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
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=password)
            if user is not None:
                user.is_active = False
                user.save()
                uidb64 = urlsafe_base64_encode(force_bytes(user.id))

                domain = get_current_site(request).domain

                link = reverse('activate', kwargs={'uidb64':uidb64, 'token': account_activation_token.make_token(user)})

                activate_url = 'http://' + domain + link

                email_body = 'Hi ' +  username +'\n'+ 'Please the link below to activate your account\n ' +activate_url + ''
                email_subject = 'Activate your account'

                email = EmailMessage(
                    email_subject,email_body,'noreply@semycolon.com',
                    [email]
                )
                email.send(fail_silently=False)
                return redirect(reverse('login'))
        if not form.is_valid():
            self.context['form_errors'] = form.errors
        return render(request, 'pages/signup.html', self.context)

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')        


class RetrieveView(View):
    context = {'pagename': 'Untitled'}

    def get(self, request: HttpRequest, access_link: str) -> HttpResponse:
        if 'author' not in request.session.keys():
            return redirect(reverse('index'))
        note = misc.retrieve_note(access_link, request.session['author'])
        source = b64decode(note.get_source().encode()).decode()
        return HttpResponse(source, content_type="text/plain")

class IndexView(View):
    context = {'pagename': 'Untitled'}

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
        note = models.Note(author=author)
        note.save()
        return JsonResponse({'init_data': note.serialize(request.session['author'])})


class DashboardView(View):
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