from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template import loader
from api.models import Note, Author
from .forms import CreateUserForm
from api.controllers import generate_authorname
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages


def index(request, name=''):
    if 'uid' not in request.session.keys():
        request.session["uid"] = None
    with open('notes/templates/ace_modes.txt', 'r') as f:
        languages = f.read().split('\n')
        context = {
            "settings": "disabled",
            "languages": languages
        }
        return render(request, 'notes/index.html', context)


def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            author = None
            if "uid" in request.session.keys():
                author = Author.objects.filter(uid=request.session["uid"])
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
        return redirect("/")
    else:
        form = CreateUserForm()
    return render(request, "notes/signup.html", {"form": form})


@login_required(login_url='login')
def userPage(request):
    try:
        notes = request.user.author.note_set.all()
    except:
        notes = None
    context = {'notes': notes}
    return render(request, "notes/userPage.html", context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('/')




def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return(redirect('/'))
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {

    }
    return render(request, 'notes/login.html', context)



