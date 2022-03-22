from rest_framework_json_api import serializers
from .models import Organization, Person, Grant, Funder, Publication, Dataset, Asset
from rest_framework_json_api.relations import ResourceRelatedField


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model"""
    class Meta:
        model = Organization
        fields = '__all__'
        depth = 1


class FunderSerializer(serializers.ModelSerializer):
    """Serializer for Funder model"""
    class Meta:
        model = Funder
        fields = '__all__'
        depth = 1


class PersonSerializer(serializers.ModelSerializer):
    """Serializer for Person model"""
    keywords = serializers.ListField(child=serializers.CharField())
    affiliations = OrganizationSerializer(read_only=True, many=True)

    def get_emails(self, obj):
        return ""

    class Meta:
        model = Person
        fields = ('id', 'affiliations', 'first_name', 'last_name', 'orcid', 'emails', 'private_emails', 'keywords')
        depth = 1


class GrantSerializer(serializers.ModelSerializer):
    """Serializer for Grant model"""
    funder_divisions = serializers.ListField(child=serializers.CharField())
    program_reference_codes = serializers.ListField(child=serializers.CharField())
    keywords = serializers.ListField(child=serializers.CharField())
    program_officials = PersonSerializer(read_only=True, many=True)
    other_investigators = PersonSerializer(read_only=True, many=True)
    principal_investigator = PersonSerializer(read_only=True, many=False)
    funder = FunderSerializer(read_only=True, many=False)
    awardee_organization = OrganizationSerializer(read_only=True, many=False)
    
    class Meta:
        model = Grant
        fields = ('id', 'award_id', 'title', 'funder', 'funder_divisions', 'program_reference_codes', 'program_officials', 'start_date', 'end_date', 'award_amount', 'principal_investigator', 'other_investigators', 'awardee_organization', 'abstract', 'keywords')

    
class PublicationSerializer(serializers.ModelSerializer):
    """Serializer for Publication model"""
    keywords = serializers.ListField(child=serializers.CharField())
    authors = PersonSerializer(read_only=True, many=True)
    grants = GrantSerializer(read_only=True, many=True)

    class Meta:
        model = Publication
        fields = ('id', 'doi', 'title', 'authors', 'grants', 'issn', 'keywords', 'language', 'publication_date', 'publication_type')
        depth = 1


class DatasetSerializer(serializers.ModelSerializer):
    authors = PersonSerializer(read_only=True, many=True)
    grants = GrantSerializer(read_only=True, many=True)
    publications = PublicationSerializer(read_only=True, many=True)

    class Meta:
        model = Dataset
        fields = ('id', 'doi', 'title', 'download_path', 'size', 'authors', 'grants', 'publications', 'mime_type')


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for Asset model"""
    keywords = serializers.ListField(child=serializers.CharField())
    author = PersonSerializer(read_only=True, many=False)
    grant = GrantSerializer(read_only=True, many=False)
    publication = PublicationSerializer(read_only=True, many=False)
    dataset = DatasetSerializer(read_only=True, many=False)
    organization = OrganizationSerializer(read_only=True, many=False)
    
    class Meta:
        model = Asset
        fields = ('id', 'doi', 'filename', 'download_path', 'size', 'author', 'grant', 'publication', 'dataset', 'organization', 'keywords', 'mime_type', 'checksum')
