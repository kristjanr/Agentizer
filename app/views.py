import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth import authenticate, login
import requests


def index(request):
    return render(request, 'app/index.html')

    #
    # <input type="checkbox">
    # <input type="hidden" name="username" value="f35583f5f9fcd7a8a13f36a10afca6aa">
    # <input type="hidden" name="password" value="ea2254154190fab7a6a33c3ec79a21f0">
    # <input type="hidden" name="text" value="A short Tour description. Accept the Tour: https://intense-tor-6246.herokuapp.com/app/respond">
    # <input type="hidden" name="to" value="+37253498963">

def send_sms(request):
    post_body = dict(
        username='f35583f5f9fcd7a8a13f36a10afca6aa',
        password='ea2254154190fab7a6a33c3ec79a21f0',
        text='A short Tour description. Accept the Tour: https://intense-tor-6246.herokuapp.com/app/respond',
        to='+37253498963',
    )
    r = requests.post('https://api2.messente.com/send_sms/', data=post_body)
    logging.warning('post response: %s', r)
    return render(request, 'app/sms_sent.html')

def respond(request):
    return render(request, 'app/respond.html')

def accepted(request):
    return render(request, 'app/accepted.html')
