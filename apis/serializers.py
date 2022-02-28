from rest_framework_json_api import serializers
from .models import Organization, Person, Grant, Funder, Publication, Dataset, Asset
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework_json_api.serializers import HyperlinkedModelSerializer


class OrganizationSerializer(HyperlinkedModelSerializer):
    """Serializer for Organization model"""
    class Meta:
        model = Organization
        fields = '__all__'


class FunderSerializer(HyperlinkedModelSerializer):
    """Serializer for Funder model"""
    class Meta:
        model = Funder
        fields = '__all__'


class AssetSerializer(HyperlinkedModelSerializer):
    """Serializer for Asset model"""
    keywords = serializers.ListField(child=serializers.CharField())

    author = ResourceRelatedField(
        model=Person,
        many=False,
        read_only=False,
        allow_null=True,
        required=False,
        queryset=Person.objects.all(),
        self_link_view_name='asset-relationships',
        related_link_view_name='asset-related',
    )

    grant = ResourceRelatedField(
        model=Grant,
        many=False,
        read_only=False,
        allow_null=True,
        required=False,
        queryset=Grant.objects.all(),
        self_link_view_name='asset-relationships',
        related_link_view_name='asset-related',
    )

    publication = ResourceRelatedField(
        model=Publication,
        many=False,
        read_only=False,
        allow_null=True,
        required=False,
        queryset=Publication.objects.all(),
        self_link_view_name='asset-relationships',
        related_link_view_name='asset-related',
    )

    dataset = ResourceRelatedField(
        model=Dataset,
        many=False,
        read_only=False,
        allow_null=True,
        required=False,
        queryset=Dataset.objects.all(),
        self_link_view_name='asset-relationships',
        related_link_view_name='asset-related',
    )

    organization = ResourceRelatedField(
        model=Organization,
        many=False,
        read_only=False,
        allow_null=True,
        required=False,
        queryset=Organization.objects.all(),
        self_link_view_name='asset-relationships',
        related_link_view_name='asset-related',
    )

    class Meta:
        model = Asset
        fields = '__all__'


class PersonSerializer(HyperlinkedModelSerializer):
    """Serializer for Person model"""
    keywords = serializers.ListField(child=serializers.CharField())

    def get_emails(self, obj):
        return ""

    class Meta:
        model = Person
        fields = '__all__'
        depth = 1

    affiliations = ResourceRelatedField(
        model=Organization,
        many=True,  
        allow_null=True,
        required=False,
        queryset=Organization.objects.all(),
        self_link_view_name='person-relationships',
        related_link_view_name='person-related',
    )    
    included_serializers = {
        'affiliations': 'apis.serializers.OrganizationSerializer',
    }


class GrantSerializer(HyperlinkedModelSerializer):
    """Serializer for Grant model"""
    funder_divisions = serializers.ListField(child=serializers.CharField())
    program_reference_codes = serializers.ListField(child=serializers.CharField())
    keywords = serializers.ListField(child=serializers.CharField())

    program_officials = ResourceRelatedField(
        model=Person,
        many=True,
        allow_null=True,
        required=False,
        queryset=Person.objects.all(),
        self_link_view_name='grant-relationships',
        related_link_view_name='grant-related',
    ) 

    other_investigators = ResourceRelatedField(
        model=Person,
        many=True,
        allow_null=True,
        required=False,
        queryset=Person.objects.all(),
        self_link_view_name='grant-relationships',
        related_link_view_name='grant-related',
    ) 

    principal_investigator = ResourceRelatedField(
        model=Person,
        many=False,
        read_only=False,
        allow_null=True,
        required=False,
        queryset=Person.objects.all(),
        self_link_view_name='grant-relationships',
        related_link_view_name='grant-related',
    )

    funder = ResourceRelatedField(
        model=Funder,
        many=False,
        read_only=False,
        allow_null=True,
        required=False,
        queryset=Funder.objects.all(),
        self_link_view_name='grant-relationships',
        related_link_view_name='grant-related',
    )

    awardee_organization = ResourceRelatedField(
        model=Organization,
        many=False,
        read_only=False,
        allow_null=True,
        required=False,
        queryset=Organization.objects.all(),
        self_link_view_name='grant-relationships',
        related_link_view_name='grant-related',
    )

    included_serializers = {
        'program_officials': 'apis.serializers.PersonSerializer',
        'other_investigators': 'apis.serializers.PersonSerializer',
        'principal_investigator': 'apis.serializers.PersonSerializer',
        'awardee_organization': 'apis.serializers.OrganizationSerializer'
    }
    
    class Meta:
        model = Grant
        fields = '__all__'

    
class PublicationSerializer(HyperlinkedModelSerializer):
    """Serializer for Publication model"""
    keywords = serializers.ListField(child=serializers.CharField())
    
    authors = ResourceRelatedField(
        model=Person,
        many=True,
        allow_null=True,
        required=False,
        queryset=Person.objects.all(),
        self_link_view_name='publication-relationships',
        related_link_view_name='publication-related',
    )  

    grants = ResourceRelatedField(
        model=Grant,
        many=True,
        allow_null=True,
        required=False,
        queryset=Grant.objects.all(),
        self_link_view_name='publication-relationships',
        related_link_view_name='publication-related',
    )  

    included_serializers = {
        'authors': 'apis.serializers.PersonSerializer',
        'grants': 'apis.serializers.GrantSerializer'
    }

    class Meta:
        model = Publication
        fields = '__all__'


class DatasetSerializer(HyperlinkedModelSerializer):
    authors = ResourceRelatedField(
        model=Person,
        many=True,
        allow_null=True,
        required=False,
        queryset=Person.objects.all(),
        self_link_view_name='dataset-relationships',
        related_link_view_name='dataset-related',
    )

    grants = ResourceRelatedField(
        model=Grant,
        many=True,
        allow_null=True,
        required=False,
        queryset=Grant.objects.all(),
        self_link_view_name='dataset-relationships',
        related_link_view_name='dataset-related',
    )  

    publications = ResourceRelatedField(
        model=Publication,
        many=True,
        allow_null=True,
        required=False,
        queryset=Publication.objects.all(),
        self_link_view_name='dataset-relationships',
        related_link_view_name='dataset-related',
    )  

    included_serializers = {
        'authors': 'apis.serializers.PersonSerializer',
        'grants': 'apis.serializers.GrantSerializer',
        'publications': 'apis.serializers.PublicationSerializer'
    }

    class Meta:
        model = Dataset
        fields = '__all__'
