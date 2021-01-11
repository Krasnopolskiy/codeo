from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from . import forms, models



class IndexView(View):
    context = {'pagename': 'index'}

    def get(self, request, name=''):
        with open('notes/templates/ace_modes.txt', 'r') as f:
            languages = f.read().split('\n')
        self.context['languages'] = languages
        return render(request, 'pages/index.html', self.context)


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


def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            author = None
            if 'uid' in request.session.keys():
                author = Author.objects.filter(uid=request.session['uid'])
                if not author.exists():
                    author = None
                if author:
                    author = author[0]
                    user.author = author
                    author.user = user
                    author.save()
            if not author:
                author = Author(uid=generate_authorname(), user=user)
                request.session['uid'] = author.uid
                user.Author = author
                author.save()
            return redirect('/login')
        return redirect('/')
    else:
        form = CreateUserForm()
    return render(request, 'pages/signup.html', {'form': form})


@login_required(login_url='login')
def userPage(request):
    try:
        notes = request.user.author.note_set.all()
    except:
        notes = None
    context = {'notes': notes}
    return render(request, 'notes/userPage.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('/')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return(redirect('/'))
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {

    }
    return render(request, 'notes/login.html', context)
