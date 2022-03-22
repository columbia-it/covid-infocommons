from rest_framework_json_api.views import ModelViewSet, RelationshipView
from .models import Person, Organization, Grant, Publication, Dataset, Asset
from .serializers import PersonSerializer, OrganizationSerializer, \
    GrantSerializer, PublicationSerializer, DatasetSerializer, AssetSerializer
from django.utils.decorators import method_decorator
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import permissions
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apis.oauth2_introspection import HasClaim
import re
from rest_framework.permissions import BasePermission
from rest_framework.schemas.openapi import AutoSchema


class ColumbiaSubClaimPermission(HasClaim):
    """
    Use OIDC 'sub' claim to determine if the subject is from the Columbia University OIDC service.
    Combine this with the preceding ColumbiaGroupClaimPermission.
    """
    claim = 'sub'
    CU_CLAIM = re.compile('.+@columbia.edu$')  # sub ends in @columbia.edu
    claims_map = {
        'GET': CU_CLAIM,
        'HEAD': CU_CLAIM,
        'OPTIONS': CU_CLAIM,
        'POST': CU_CLAIM,
        'PATCH': CU_CLAIM,
        'DELETE': CU_CLAIM,
    }


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
    permission_classes = (ColumbiaSubClaimPermission,) # specify the permission class in your view
    
    schema = AutoSchema(
        tags=['organizations'],
    )

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
    serializer_class = AssetSerializer

    schema = AutoSchema(
        tags=['assets'],
    )


class AssetRelationshipView(RelationshipView):
    """
    View for asset.relationships
    """
    queryset = Asset.objects
    self_link_view_name = 'asset-relationships'

    schema = AutoSchema(
        tags=['assets'],
    )


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
    serializer_class = PersonSerializer

    schema = AutoSchema(
        tags=['people'],
    )


class PersonRelationshipView(RelationshipView):
    """
    View for person.relationships
    """
    queryset = Person.objects
    self_link_view_name = 'person-relationships'

    schema = AutoSchema(
        tags=['people'],
    )


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
    serializer_class = GrantSerializer

    schema = AutoSchema(
        tags=['grants'],
    )


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
    serializer_class = PublicationSerializer

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
    serializer_class = DatasetSerializer

    schema = AutoSchema(
        tags=['datasets'],
    )
    