

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/', views.dologin_view, name='login_user'),
    url(r'^login/', views.login_view, name='login_view'),
    url(r'^guides/', views.guides, name='guides'),
]