from rest_framework_json_api import serializers
from .models import Organization, Person, Grant, Funder, Publication, Dataset, Asset
from rest_framework_json_api.relations import ResourceRelatedField


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model"""
    class Meta:
        model = Organization
        fields = '__all__'


class FunderSerializer(serializers.ModelSerializer):
    """Serializer for Funder model"""
    class Meta:
        model = Funder
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    """Serializer for Person model"""

    def get_emails(self, obj):
        return ""

    class Meta:
        model = Person
        fields = ('id', 'affiliations', 'first_name', 'last_name', 'orcid', 'emails', 'private_emails', 'keywords')
        depth = 1


class CreatePersonSerializer(serializers.ModelSerializer):
    """Serializer for Person model"""
    keywords = serializers.ListField(child=serializers.CharField(), required=False)

    def get_emails(self, obj):
        return ""

    class Meta:
        model = Person
        fields = ('id', 'affiliations', 'first_name', 'last_name', 'orcid', 'emails', 'private_emails', 'keywords')


class GrantSerializer(serializers.ModelSerializer):
    """Serializer for Grant model"""
    
    class Meta:
        model = Grant
        fields = ('id', 'award_id', 'title', 'funder', 'funder_divisions', 'program_reference_codes', 'program_officials', 'start_date', 'end_date', 'award_amount', 'principal_investigator', 'other_investigators', 'awardee_organization', 'abstract', 'keywords')
        depth = 1


class CreateGrantSerializer(serializers.ModelSerializer):
    """Serializer for Grant model"""
    funder_divisions = serializers.ListField(child=serializers.CharField(), required=False)
    program_reference_codes = serializers.ListField(child=serializers.CharField(), required=False)
    keywords = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = Grant
        fields = ('id', 'award_id', 'title', 'funder', 'funder_divisions', 'program_reference_codes', 'program_officials', 'start_date', 'end_date', 'award_amount', 'principal_investigator', 'other_investigators', 'awardee_organization', 'abstract', 'keywords')

    
class PublicationSerializer(serializers.ModelSerializer):
    """Serializer for Publication model"""

    class Meta:
        model = Publication
        fields = ('id', 'doi', 'title', 'authors', 'grants', 'issn', 'keywords', 'language', 'publication_date', 'publication_type')
        depth = 1


class CreatePublicationSerializer(serializers.ModelSerializer):
    """Serializer for Publication model"""
    keywords = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Publication
        fields = ('id', 'doi', 'title', 'authors', 'grants', 'issn', 'keywords', 'language', 'publication_date', 'publication_type')


class DatasetSerializer(serializers.ModelSerializer):
    """Serializer for Dataset model"""
    class Meta:
        model = Dataset
        fields = ('id', 'doi', 'title', 'download_path', 'size', 'authors', 'grants', 'publications', 'mime_type')
        depth = 1


class CreateDatasetSerializer(serializers.ModelSerializer):
    """Serializer for create Dataset model"""
    class Meta:
        model = Dataset
        fields = ('id', 'doi', 'title', 'download_path', 'size', 'authors', 'grants', 'publications', 'mime_type')


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for Asset model"""
    
    class Meta:
        model = Asset
        fields = ('id', 'doi', 'filename', 'download_path', 'size', 'author', 'grant', 'publication', 'dataset', 'organization', 'keywords', 'mime_type', 'checksum')
        depth = 1


class CreateAssetSerializer(serializers.ModelSerializer):
    """Serializer for Asset model"""
    keywords = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = Asset
        fields = ('id', 'doi', 'filename', 'download_path', 'size', 'author', 'grant', 'publication', 'dataset', 'organization', 'keywords', 'mime_type', 'checksum')
