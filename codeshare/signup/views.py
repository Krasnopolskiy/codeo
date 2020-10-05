from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def signup(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/home")
    else:
        form = UserCreationForm
    form = UserCreationForm()
    return render(response, "registration/signup.html", {"form":form})
