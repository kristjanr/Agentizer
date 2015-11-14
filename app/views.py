from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'app/index.html')


def guides(request):
    return render(request, 'app/guides.html')
