from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^login/$', 'pscore.auth.views.login'),
    url(r'^callback/$', 'pscore.auth.views.callback'),
)
