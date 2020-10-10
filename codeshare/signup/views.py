from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from api.models import Author
from django.contrib.auth.decorators import login_required
from api.controllers import generate_authorname
from .forms import CreateUserForm
#from .decorators import allowed_users
def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if "uid" in request.session.keys():
                author = Author.objects.filter(uid=request.session["uid"])
                if not author.exists():
                    author = None
                else:
                    author = author[0]
                    user.author = author
                    author.user = user
                    author.save()

            return redirect('/login')
        return redirect("/home")
    else:
        form = CreateUserForm()
    return render(request, "registration/signup.html", {"form":form})

@login_required(login_url = 'login')
def userPage(request):
    try:
        notes = request.user.author.note_set.all()
    except:
        notes = None
    context = {'notes':notes}
    return render (request, "registration/userPage.html", context)



