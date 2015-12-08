from django.conf.urls import patterns, url, include

from app import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='home'),
   url(r'^account/signup/$', views.SignupView.as_view(), name="account_signup"),
   url(r'^account/', include("account.urls")),
   url(r'^tour/add$', views.tour, name='add_tour'),
   url(r'^tour/(?P<tour_id>[0-9]+)/$', views.tour, name='tour'),
   url(r'^tour/(?P<tour_id>[0-9]+)/guides$', views.add_guides, name='add_guides'),
   url(r'^send_sms', views.send_sms, name='send_sms'),
   url(r'^respond', views.respond, name='respond'),
   url(r'^answer', views.answer, name='answer'),
   url(r'^show_guide_tour_details', views.show_guide_tour_details, name='show_guide_tour_details'),
)
