from django.conf.urls import patterns, url, include

from app import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^tour', views.tour, name='tour'),
   url(r'^guides', views.guides, name='guides'),
   url(r'^send_sms', views.send_sms, name='send_sms'),
   url(r'^respond', views.respond, name='respond'),
   url(r'^accepted', views.accepted, name='accepted'),

)
