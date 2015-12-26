from account.decorators import login_required
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from app.mobile_views import respond, answer
from app.views import SignupView, send_sms, TourListView, add_or_edit_tour, TourDetailView, add_guides, GuideListView, GuideCreateView, GuideUpdate, GuideDelete

urlpatterns = patterns('',
   url(r'^$', TemplateView.as_view(template_name='app/index.html'), name='home'),
   url(r'^account/signup/$', SignupView.as_view(), name='account_signup'),
   url(r'^account/', include('account.urls')),
   url(r'^send_sms', send_sms, name='send_sms'),
   url(r'^respond', respond, name='respond'),
   url(r'^answer', answer, name='answer'),
   url(r'^tour/$', TourListView.as_view(template_name='app/tour_list.html'), name='tours'),
   url(r'^tour/add$', add_or_edit_tour, name='add_tour'),
   url(r'^tour/(?P<tour_id>[0-9]+)/$', add_or_edit_tour, name='edit_tour'),
   url(r'^tour/(?P<pk>[0-9]+)/view$', login_required(TourDetailView.as_view()), name='view_tour'),
   url(r'^tour/(?P<tour_id>[0-9]+)/guides$', add_guides, name='add_guides'),
   url(r'^guide/$', GuideListView.as_view(), name='guides'),
   url(r'^guide/add/$', GuideCreateView.as_view(), name='guide-add'),
   url(r'^guide/(?P<pk>[0-9]+)/$', GuideUpdate.as_view(), name='guide-update'),
   url(r'^guide/(?P<pk>[0-9]+)/delete/$', GuideDelete.as_view(), name='guide-delete'),
)
