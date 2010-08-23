from django.contrib import auth
from django.contrib.auth.middleware import LazyUser
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.http import HttpResponseRedirect

from odesk import Client, HTTP400BadRequestError


class ClientMiddleware(object):

    def process_request(self, request):
        """
        Injects an initialized oDesk client to every request, making 
        it easy to use it in views
        """
        api_token = request.session.get('odesk_api_token', None) 
        request.odesk_client = Client(settings.ODESK_PUBLIC_KEY, 
                                      settings.ODESK_PRIVATE_KEY,
                                      api_token)
        request.__class__.user = LazyUser()
        request.__class__.odesk_user = ''
        return None

        
class AuthMiddleware(object):

    def process_request(self, request):
        if 'odesk_user' in request.session:
            request.odesk_user = request.session['odesk_user']
        
        if request and request.user.is_authenticated():
            return None
        
        if not request.odesk_user is AnonymousUser:
            user = auth.authenticate(odesk_user=request.odesk_user)
            if user:
                request.user = user
                auth.login(request, user)
        
        return None

    def clean_username(self, username, request):
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError: # Backend has no clean_username method.
            pass
        return username    
