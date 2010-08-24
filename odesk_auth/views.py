from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as django_logout

def login(request):
    if 'odesk_api_token' in request.session:
        del request.session['odesk_api_token']
    request.odesk_client.api_token = None
    return HttpResponseRedirect(request.odesk_client.auth.auth_url())


def callback(request, redirect_url=None):
    frob = request.GET.get('frob', None)
    if frob:
        api_token, auth_user = request.odesk_client.auth.get_token(frob) 
        request.session['odesk_api_token'] = api_token
        request.session['odesk_user'] = auth_user
        
        if not request.odesk_user is AnonymousUser:
            user = auth.authenticate(odesk_user=request.odesk_user)
            if user:
                request.user = user
                
        redirect_url = request.session.pop('odesk_redirect_url', redirect_url)
        if not redirect_url:
            redirect_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')   
        return HttpResponseRedirect(redirect_url)
    
    else:
        return HttpResponseRedirect(request.odesk_client.auth.auth_url())
    

def logout(request):
    if 'odesk_api_token' in request.session:
        del request.session['odesk_api_token']
    request.odesk_client.auth.revoke_token()
    if request.user.is_authenticated():
        django_logout(request)
    return HttpResponseRedirect(request.odesk_client.auth.auth_url())
    