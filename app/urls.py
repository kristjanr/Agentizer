

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send_sms', views.send_sms, name='send_sms'),
    url(r'^respond', views.respond, name='respond'),
    url(r'^accept', views.accepted, name='accepted'),
]