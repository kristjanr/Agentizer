from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'app/index.html')


def send_sms(request):

    return render(request, 'app/sms_sent.html')

def respond(request):
    return render(request, 'app/respond.html')

def accepted(request):
    return render(request, 'app/accepted.html')
