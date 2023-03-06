import imp
from urllib import request
from rest_framework_json_api.views import ModelViewSet, RelationshipView
from .models import Person, Organization, Grant, Publication, Dataset, Asset
from .serializers import PersonSerializer, OrganizationSerializer, \
    GrantSerializer, PublicationSerializer, DatasetSerializer, AssetSerializer, CreatePersonSerializer, CreateGrantSerializer, CreatePublicationSerializer, CreateDatasetSerializer, CreateAssetSerializer
from django.utils.decorators import method_decorator
from apis.oauth2_introspection import HasClaim
import re
from rest_framework.schemas.openapi import AutoSchema
from search.utils import update_grant_in_index
from rest_framework.response import Response

usual_rels = ('exact', 'lt', 'gt', 'gte', 'lte', 'in')
text_rels = ('icontains', 'iexact', 'contains')


class OrganizationViewSet(ModelViewSet):
    """ View for Organization APIs
    retrieve:
    Return the given Organization.

    list:
    Return a list of all the Organizations.

    create:
    Create a new Organization instance.

    destroy:
    Delete a given Organization instance
    """
    __doc__ = Organization.__doc__
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    
    schema = AutoSchema(
        tags=['organizations'],
    )

    filterset_fields = {
        'ror': usual_rels + text_rels,
        'name': usual_rels + text_rels
    }

class AssetViewSet(ModelViewSet):
    """ View for Asset APIs
    retrieve:
    Return the given Asset.

    list:
    Return a list of all the Assets.

    create:
    Create a new Asset instance.

    destroy:
    Delete a given Asset instance
    """
    __doc__ = Asset.__doc__
    queryset = Asset.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return CreateAssetSerializer
        return AssetSerializer

    schema = AutoSchema(
        tags=['assets'],
    )

    filterset_fields = {
        'author__id': usual_rels + text_rels,
        'grant__id': usual_rels + text_rels,
        'publication__id': usual_rels + text_rels,
        'organization__id': usual_rels + text_rels,
        'dataset__id': usual_rels + text_rels
    }


class PersonViewSet(ModelViewSet):
    """ View for Person APIs
    retrieve:
    Return the given Person.

    list:
    Return a list of all the people.

    create:
    Create a new Person instance.

    destroy:
    Delete a given Person instance
    """
    __doc__ = Person.__doc__
    queryset = Person.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return CreatePersonSerializer
        return PersonSerializer
    
    schema = AutoSchema(
        tags=['people'],
    )

    filterset_fields = {
        'orcid': usual_rels + text_rels,
        'emails': usual_rels + text_rels,
        'private_emails': usual_rels + text_rels,
        'last_name': usual_rels + text_rels
    }


class GrantViewSet(ModelViewSet):
    """ View for Grant APIs
    retrieve:
    Return the given Grant.

    list:
    Return a list of all the grants.

    create:
    Create a new Grant instance.

    destroy:
    Delete a given Grant instance
    """
    __doc__ = Grant.__doc__
    queryset = Grant.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return CreateGrantSerializer
        return GrantSerializer

    schema = AutoSchema(
        tags=['grants'],
    )
 
    def update(self, request, *args, **kwargs):
        try:
            super().update(request, *args, **kwargs)
            instance = self.get_object()
            print(instance)
            update_grant_pi_in_index(instance)
        except:
            return Response(status_code=400)
        return Response(GrantSerializer(instance).data)



class PublicationViewSet(ModelViewSet):
    """ View for Publication APIs
    retrieve:
    Return the given Publication.

    list:
    Return a list of all the Publications.

    create:
    Create a new Publication instance.

    destroy:
    Delete a given Publication instance
    """
    __doc__ = Publication.__doc__
    queryset = Publication.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return CreatePublicationSerializer
        return PublicationSerializer

    schema = AutoSchema(
        tags=['publications'],
    )


class DatasetViewSet(ModelViewSet):
    """ View for Dataset APIs
    retrieve:
    Return the given Dataset.

    list:
    Return a list of all the Datasets.

    create:
    Create a new Dataset instance.

    destroy:
    Delete a given Dataset instance
    """
    __doc__ = Dataset.__doc__
    queryset = Dataset.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return CreateDatasetSerializer
        return DatasetSerializer

    schema = AutoSchema(
        tags=['datasets'],
    )
    