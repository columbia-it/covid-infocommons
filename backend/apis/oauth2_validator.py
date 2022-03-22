from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):

    """
    Extend the ID Token and Userinfo claims
    """
    def get_additional_claims(self, request):
        """
        Return additional ID Token Claims based on the OIDC scope claims.
        Args:
            request:

        Returns:
            dict of additional claims
        """
        claims = {
            "sub": request.user.username
        }
        if 'profile' in request.scopes:
            claims["given_name"] = request.user.first_name
            claims["family_name"] = request.user.last_name
            claims["name"] = ' '.join([request.user.first_name, request.user.last_name])
        if 'email' in request.scopes:
            claims["email"] = request.user.email
        if 'https://api.columbia.edu/scope/group' in request.scopes:
            claims['https://api.columbia.edu/claim/group'] = ' '.join([g.name for g in request.user.groups.all()])
        return claims
