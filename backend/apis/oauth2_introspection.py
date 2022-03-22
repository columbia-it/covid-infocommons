from attr import has
from rest_framework.permissions import BasePermission
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.settings import oauth2_settings
import requests
import json
import re
from oauth2_provider.models import get_access_token_model
from django.contrib.auth.models import User

AccessToken = get_access_token_model()
SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class HasClaim(BasePermission, OAuthLibMixin):

    claim = None
    #: map by HTTP method of which word in the claim must be present.
    #: claim values are assumed to be a string list of words (similar to scopes) or RE.
    claims_map = {
        'GET': None,
        'OPTIONS': None,
        'HEAD': None,
        'POST': None,
        'PUT': None,
        'PATCH': None,
        'DELETE': None,
    }
    
    def __init__(self):
        """
        See if our OAuth2/OIDC AS even has the userinfo endpoint
        """
        self.userinfo_url = oauth2_settings.OIDC_USERINFO_ENDPOINT
 
    def _get_claims_from_authentication_server(self, request):
        user_info = {}
        print('*** 3 ***')
        bearer_token = request.headers.get('Authorization').split(' ')[1]
        print('*** 4 ***')
        try:
            response = requests.get(self.userinfo_url, headers={'Authorization': 'Bearer {}'.format(bearer_token)})
            print('***  ***')
        except requests.exceptions.RequestException:
            return None
        
        if response.status_code == 200:
            user_info = response.content.decode('utf-8')
            return user_info
        return None

    
    def has_permission(self, request, view):
        """
        If an OIDC `claim` name was configured along with a `claim_map` that looks for a given claim value
        then return true if the claim value is present in the userinfo response.
        If the mapping is None then return False.
        If the mapping is the empty string then return True.
        """
        print('*** oauth2_introspection.has_permission() ***')
        if request.method in SAFE_METHODS:
            return True

        user_has_permission = False

        if self.claim is None:
            assert False, 'HasClaim called but not configured.'

        if request.method in self.claims_map:
            print('HasClaim: looking for {} claim {} value "{}"'
                      .format(request.method, self.claim, self.claims_map.get(request.method)))

        if (request.method in self.claims_map
            and request.headers.get('Authorization')):            
            # if request.auth.userinfo is None:
            if self.userinfo_url:
                user_info_str = self._get_claims_from_authentication_server(request)
                if user_info_str:
                    user_info = json.loads(user_info_str)
                    logged_in_user = User.objects.all().filter(username=user_info.get('sub'))[0]
                    # For now just check by group name. TODO - check if user has specific model permission
                    if logged_in_user.groups.filter(name = 'editor').exists():
                        user_has_permission = True

                try:
                    claims_map_entry = self.claims_map[request.method]
                    if claims_map_entry is None:
                        print('Claim denied (None means False)')  # TODO: change up to use True/False?
                        return False
                    if claims_map_entry == '':
                        print('Claim approved (empty string means True)')
                        claim_approved = True
                        return (True and user_has_permission)
                    claim_value = user_info.get('sub')

                    if type(claims_map_entry) == str:
                        claims = claim_value.split()
                        if claims_map_entry in claims:
                            print('Claim approved ("{}" is in {})'.format(claims_map_entry, claims))
                            return (True and user_has_permission)
                        else:
                            print('Claim denied ("{}" not in {})'.format(claims_map_entry, claims))
                            return False
                    elif type(claims_map_entry) == re.Pattern:
                        if claims_map_entry.match(claim_value):
                            print('Claim approved ("{}" matches {})'.format(claim_value, claims_map_entry))
                            return (True and user_has_permission)
                        else:
                            print('Claim denied ("{}" does not match {})'.format(claim_value, claims_map_entry))
                            return False
                    else:
                        print('claim value must be of type str or re')
                        return False
                except Exception as e:
                    print(e)
                    return False
            else:
                return False