from rest_framework_json_api import serializers
from .models import Organization, Person, Grant, Funder, Publication, Dataset, Asset
from rest_framework_json_api.relations import ResourceRelatedField


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model"""
    class Meta:
        model = Organization
        fields = '__all__'
        depth = 2


class FunderSerializer(serializers.ModelSerializer):
    """Serializer for Funder model"""
    class Meta:
        model = Funder
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    """Serializer for Person model"""
    keywords = serializers.ListField(child=serializers.CharField(), required=False)

    def get_emails(self, obj):
        return ""

    class Meta:
        model = Person
        fields = ('id', 'affiliations', 'first_name', 'last_name', 'orcid', 'emails', 'private_emails', 'keywords', 'approved', 'desired_collaboration', 'comments', 'websites')
        depth = 2


class CreatePersonSerializer(serializers.ModelSerializer):
    """Serializer for Person model"""
    keywords = serializers.ListField(child=serializers.CharField(), required=False)

    def get_emails(self, obj):
        return ""

    class Meta:
        model = Person
        fields = ('id', 'affiliations', 'first_name', 'last_name', 'orcid', 'emails', 'private_emails', 'keywords', 'approved', 'desired_collaboration', 'comments')


class FunderDivisionListField(serializers.Field):
    def to_internal_value(self, data):
        """
        Replace , with \t in the data (if any) during de-serialization
        """
        for i in range(len(data)):
            if ',' in data[i]:
                data[i] = data[i].replace(',', '\t')
        return data

    def to_representation(self, value):
        """
        Replace \t with , in the value (if any) during serialization
        """
        for i in range(len(value)):
            if '\t' in value[i]:
                value[i] = value[i].replace('\t', ',')
        return value


class GrantSerializer(serializers.ModelSerializer):
    """Serializer for Grant model"""
    keywords = serializers.ListField(child=serializers.CharField(), required=False)
    funder_divisions = FunderDivisionListField()
    program_reference_codes = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Grant
        fields = ('id', 'award_id', 'title', 'funder', 'funder_divisions', 'program_reference_codes', 'program_officials', 'start_date', 'end_date', 'award_amount', 'principal_investigator', 'other_investigators', 'awardee_organization', 'abstract', 'keywords', 'approved')
        depth = 2


class CreateGrantSerializer(serializers.ModelSerializer):
    """Serializer for Grant model"""
    funder_divisions = FunderDivisionListField()
    program_reference_codes = serializers.ListField(child=serializers.CharField(), required=False)
    keywords = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Grant
        fields = ('id', 'award_id', 'title', 'funder', 'funder_divisions', 'program_reference_codes', 'program_officials', 'start_date', 'end_date', 'award_amount', 'principal_investigator', 'other_investigators', 'awardee_organization', 'abstract', 'keywords', 'approved')

    
class PublicationSerializer(serializers.ModelSerializer):
    """Serializer for Publication model"""

    class Meta:
        model = Publication
        fields = ('id', 'doi', 'title', 'authors', 'grants', 'issn', 'keywords', 'language', 'publication_date', 'publication_type')
        depth = 2


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
        fields = ('id', 'doi', 'filename', 'download_path', 'size', 'author', 'grant', 'publication', 'dataset', 'organization', 'keywords', 'mime_type', 'checksum', 'approved')
        depth = 1


class CreateAssetSerializer(serializers.ModelSerializer):
    """Serializer for Asset model"""
    keywords = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = Asset
        fields = ('id', 'doi', 'filename', 'download_path', 'size', 'author', 'grant', 'publication', 'dataset', 'organization', 'keywords', 'mime_type', 'checksum', 'approved')
