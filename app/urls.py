from account.decorators import login_required
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from app import views
import app.views

urlpatterns = patterns('',
   url(r'^$', TemplateView.as_view(template_name='app/index.html'), name='home'),
   url(r'^account/signup/$', views.SignupView.as_view(), name='account_signup'),
   url(r'^account/', include('account.urls')),
   url(r'^tour/$', views.TourListView.as_view(template_name='app/tour_list.html'), name='tours'),
   url(r'^tour/add$', views.add_or_edit_tour, name='add_tour'),
   url(r'^tour/(?P<tour_id>[0-9]+)/$', views.add_or_edit_tour, name='edit_tour'),
   url(r'^tour/(?P<tour_id>[0-9]+)/guides$', views.add_guides, name='add_guides'),
   url(r'^send_sms', views.send_sms, name='send_sms'),
   url(r'^respond', app.views.respond, name='respond'),
   url(r'^answer', app.views.answer, name='answer'),
   url(r'^tour/(?P<pk>[0-9]+)/readonly', login_required(views.TourDetailView.as_view()), name='tour-detail'),
)
