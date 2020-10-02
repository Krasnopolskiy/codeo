from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def signup(response):
    form = UserCreationForm()
    return render(response, "registration/signup.html", {"form":form})
