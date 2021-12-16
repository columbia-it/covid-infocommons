from rest_framework import viewsets
from .models import Person, Organization, Grant
from .serializers import PersonSerializer, OrganizationSerializer, CreatePersonSerializer, \
    GrantSerializer, CreateGrantSerializer
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='All people available in CIC',
    operation_summary='Get list of all people'))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description='You must be logged in. Use the JSON structure and schema as shown below.',
    operation_summary='Create a new person'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='Get a person',
    operation_summary='Get a person'))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description='Update person metadata for a given id',
    operation_summary='Update person metadata for a given id'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description='Remove a person',
    operation_summary='Remove a person'))
class PersonViewSet(viewsets.ModelViewSet):
    """ View for Person APIs
    retrieve:
    Return the given Person.

    list:
    Return a list of all the people.

    create:
    Create a new person instance.

    destroy:
    Delete a given person instance
    """
    queryset = Person.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return PersonSerializer
        if self.action == 'create':
            return CreatePersonSerializer

    http_method_names = ['get', 'post', 'delete', 'put']


@method_decorator(name='list', decorator=swagger_auto_schema(operation_description='All organizations available in CIC'))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description='You must be logged in. Use the JSON structure and schema as shown below.'))
class OrganizationViewSet(viewsets.ModelViewSet):
    """ View for Organization APIs
    retrieve:
    Return the given Person.

    list:
    Return a list of all the people.

    create:
    Create a new person instance.

    destroy:
    Delete a given person instance
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    http_method_names = ['get', 'post', 'delete', 'put']


REQUIRED_SCOPES_ALTS = {
    'GET': [['auth-columbia', 'read'], ['auth-none', 'read']],
    'HEAD': [['read']],
    'OPTIONS': [['read']],
    'POST': [
        ['auth-columbia', 'demo-netphone-admin', 'create'],
        ['auth-none', 'demo-netphone-admin', 'create'],
    ]
}


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='All grants available in CIC',
    operation_summary='Get list of all grants',
    responses={200: GrantSerializer(many=True)}))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description='You must be logged in. Use the JSON structure and schema as shown below.',
    operation_summary='Create a new grant'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='Get a grant',
    operation_summary='Get a grant'))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description='Update grant metadata for a given id',
    operation_summary='Update grant metadata for a given id'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description='Remove a grant',
    operation_summary='Remove a grant'))
class GrantViewSet(viewsets.ModelViewSet):
    """ View for Grant APIs
    retrieve:
    Return the given Person.

    list:
    Return a list of all the people.

    create:
    Create a new person instance.

    destroy:
    Delete a given person instance
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)
    queryset = Grant.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return GrantSerializer
        if self.action == 'create':
            return CreateGrantSerializer

    http_method_names = ['get', 'post', 'delete', 'put']
