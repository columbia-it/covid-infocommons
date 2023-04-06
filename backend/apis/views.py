import imp
import logging
from multiprocessing import context
from urllib import request
from rest_framework_json_api.views import ModelViewSet, RelationshipView
from .models import Person, Organization, Grant, Publication, Dataset, Asset
from .serializers import PersonSerializer, OrganizationSerializer, \
    GrantSerializer, PublicationSerializer, DatasetSerializer, AssetSerializer, CreatePersonSerializer, CreateGrantSerializer, CreatePublicationSerializer, CreateDatasetSerializer, CreateAssetSerializer
from django.utils.decorators import method_decorator
from apis.oauth2_introspection import HasClaim
import re
from rest_framework.schemas.openapi import AutoSchema
from search.utils import update_person_in_grant_index, update_grant_in_grant_index
from rest_framework.response import Response
from rest_framework_json_api.exceptions import exception_handler

logger = logging.getLogger(__name__)

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

    # Override update/PATCH request so we can update search index
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            update_person_in_grant_index(instance)
            return Response(PersonSerializer(instance).data)
        except Exception as e:
            logger.error('Error occurred while updating Person')
            return exception_handler(e, context)


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

    # Override update/PATCH request so we can update search index
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            update_grant_in_grant_index(instance)
            return Response(GrantSerializer(instance).data)
        except Exception as e:
            logger.error('Error occurred while updating Grant')
            return exception_handler(e, context)


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
    