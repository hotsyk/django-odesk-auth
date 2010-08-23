from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, check_password
from django.db import models

from odesk import Client, HTTP400BadRequestError


class ODeskAPIAuthBackend:
    # Create a User object if not already in the database?
    create_unknown_user = True
        
    def authenticate(self, odesk_user):
        """
        The user passed as ``odesk_user`` is considered trusted and
        authenticated via middleware.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not odesk_user:
            return
        user = None
        username = self.clean_username(odesk_user['uid'])

        if not getattr(settings, 'AUTH_USER_MODULE', False):
            UserModel = models.get_model('auth', 'User')
        else:
            try:
                app_label, model_name = settings.AUTH_USER_MODULE.split('.')
                UserModel = models.get_model(app_label, model_name)
            except:
                UserModel = models.get_model('auth', 'User')
                
        if self.create_unknown_user:
            user, created = UserModel.objects.get_or_create(username=username)
            if created:
                user = self.configure_user(user)
        else:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                pass
            
        if user:
            user.first_name = odesk_user['first_name']
            user.last_name = odesk_user['last_name']
            user.email = odesk_user['mail']
            user.save()
            
            try:
                profile = user.get_profile()
            except:
                profile = None
                                
        return user
    

    def clean_username(self, username):
        return username.encode('utf-8')

    def configure_user(self, user):
        try:
            profile = user.get_profile()
        except:
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                profile = None
            else:
                try:
                    app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
                    UserProfile = models.get_model(app_label, model_name)
                    profile = UserProfile.objects.create(user=user,\
                                                    odesk_userid=user.username)
                    profile.save()
                    
                except:
                    profile = None        
        return user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(username=user_id)
        except:
            return None