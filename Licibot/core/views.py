from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.

def home (request):
    return render(request, 'home.html')

