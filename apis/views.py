from rest_framework_json_api.views import ModelViewSet, RelationshipView
from .models import Person, Organization, Grant, Publication, Dataset, Asset
from .serializers import PersonSerializer, OrganizationSerializer, \
    GrantSerializer, PublicationSerializer, DatasetSerializer, AssetSerializer
from django.utils.decorators import method_decorator


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


class PersonRelationshipView(RelationshipView):
    """
    View for person.relationships
    """
    queryset = Person.objects
    self_link_view_name = 'person-relationships'


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


class GrantRelationshipView(RelationshipView):
    """
    View for grant.relationships
    """
    queryset = Grant.objects
    self_link_view_name = 'grant-relationships'


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


class PublicationRelationshipView(RelationshipView):
    """
    View for publication.relationships
    """
    queryset = Publication.objects
    self_link_view_name = 'publication-relationships'


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


class DatasetRelationshipView(RelationshipView):
    """
    View for dataset.relationships
    """
    queryset = Dataset.objects
    self_link_view_name = 'dataset-relationships'