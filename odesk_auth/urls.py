from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^login/$', 'odesk_auth.views.login'),
    url(r'^callback/$', 'odesk_auth.views.callback'),
    url(r'^logout/$', 'odesk_auth.views.logout'),
)
