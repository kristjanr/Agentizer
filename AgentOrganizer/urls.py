from django.conf.urls import patterns, url, include
from django.contrib import admin

urlpatterns = patterns('',
   url(r'^', include('app.urls')),
   url(r'^admin/', include(admin.site.urls)),
)
