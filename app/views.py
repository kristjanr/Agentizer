import logging

from django.shortcuts import render
import requests

sms_text = 'Garage48 Tours job offer on 20.11.2015 at 10:00-13:00.\nPlease confirm here: http://www.agentizer.com/respond?uid=[uid]'

def index(request):
    return render(request, 'app/index.html')


def tour(request):
    return render(request, 'app/tour.html')


def guides(request):
    return render(request, 'app/guides.html', context=dict(sms_text=sms_text))


def send_sms(request):
    post_body = {
        'username': 'f35583f5f9fcd7a8a13f36a10afca6aa',
        'password': 'ea2254154190fab7a6a33c3ec79a21f0',
        'text': sms_text,
        'from': 'Agentizer',
        'to': '+37253498963',
    }
    r = requests.post('http://api2.messente.com/send_sms/', data=post_body)
    logging.warning('post response: %s', r.content)
    return render(request, 'app/sms_sent.html')


def respond(request):
    return render(request, 'app/respond.html')


def accepted(request):
    return render(request, 'app/accepted.html')
