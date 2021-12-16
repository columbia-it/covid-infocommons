from rest_framework import serializers
from .models import Organization, Person, Grant, Funder


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
    affiliations = OrganizationSerializer(many=True, required=False, read_only=True)
    emails = serializers.SerializerMethodField()

    def get_emails(self, obj):
        return ""

    class Meta:
        model = Person
        fields = '__all__'
        depth = 1


class CreatePersonSerializer(serializers.ModelSerializer):
    """Serializer for Person model - Used with Person creation"""
    class Meta:
        model = Person
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        affiliations = []
        for affiliation in data['affiliations']:
            affiliations.append(OrganizationSerializer(Organization.objects.get(pk=affiliation)).data)
        data['affiliations'] = affiliations
        return data


class GrantSerializer(serializers.ModelSerializer):
    """Serializer for Grant model"""

    funder = FunderSerializer(read_only=True)
    principal_investigator = PersonSerializer(read_only=True)
    program_officials = PersonSerializer(many=True, read_only=True)
    other_investigators = PersonSerializer(many=True, read_only=True)
    awardee_organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Grant
        fields = '__all__'


class CreateGrantSerializer(serializers.ModelSerializer):
    """Serializer for Grant model - Used with Grant creation"""
    class Meta:
        model = Grant
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['funder'] = FunderSerializer(
            Funder.objects.get(pk=data['funder'])).data

        program_officials = []
        for person_id in data['program_officials']:
            program_officials.append(PersonSerializer(Person.objects.get(pk=person_id)).data)
        data['program_officials'] = program_officials

        data['principal_investigator'] = PersonSerializer(Person.objects.get(
            pk=data['principal_investigator'])).data

        other_investigators = []
        for other_investigator_id in data['other_investigators']:
            other_investigators.append(PersonSerializer(Person.objects.get(pk=other_investigator_id)).data)
        data['other_investigators'] = other_investigators

        data['awardee_organization'] = OrganizationSerializer(
            Organization.objects.get(pk=data['awardee_organization'])).data

        return data
