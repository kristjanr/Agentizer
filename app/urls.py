from django.conf.urls import patterns, url, include

from app import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='home'),
   url(r'^tour$', views.create_tour, name='tour'),
   url(r'^guides', views.guides, name='guides'),
   url(r'^send_sms', views.send_sms, name='send_sms'),
   url(r'^respond', views.respond, name='respond'),
   url(r'^answer', views.answer, name='answer'),
   url(r'^tour_details', views.tour_details, name='tour_details'),
)
