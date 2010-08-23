from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from odesk_auth.models import *

#Quick and dirty decorator. Should be rewritten with functools
def auth_required(function):
    def wrapped(request, *args, **kwargs):
        if not request.odesk_client.auth.check_token():
            return HttpResponseRedirect(getattr(settings, 'LOGIN_URL', '/'))
        return function(request, *args, **kwargs)
    return wrapped