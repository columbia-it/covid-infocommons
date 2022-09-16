from gettext import install
import json
from operator import concat
from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from apis.models import Grant, Funder, Person, Organization


@registry.register_document
class GrantDocument(Document):

    @staticmethod
    def get_organization_properties():
        return {
            'id': fields.IntegerField(),
            'ror': fields.KeywordField(),
            'name': fields.KeywordField(),
            'address': fields.KeywordField(),
            'city': fields.KeywordField(),
            'state': fields.KeywordField(),
            'zip': fields.KeywordField(),
            'country': fields.KeywordField(),
            'approved': fields.BooleanField()
        }

    @staticmethod
    def get_person_properties():
        return {
            'id': fields.IntegerField(),
            'first_name': fields.KeywordField(),
            'last_name': fields.KeywordField(),
            'full_name': fields.KeywordField(),
            'orcid': fields.KeywordField(),
            'emails': fields.KeywordField(),
            'private_emails': fields.KeywordField(),
            'keywords': fields.KeywordField(),
            'full_name': fields.KeywordField(),
            'approved': fields.BooleanField(),
            'websites': fields.KeywordField(),
            'desired_collaboration': fields.KeywordField(),
            'comments': fields.KeywordField(),
            'affiliations': fields.NestedField(properties = {
                'id': fields.IntegerField(),
                'ror': fields.KeywordField(),
                'name': fields.KeywordField(),
                'address': fields.KeywordField(),
                'city': fields.KeywordField(),
                'state': fields.KeywordField(),
                'zip': fields.KeywordField(),
                'country': fields.KeywordField(),
                'approved': fields.BooleanField()
            })
        }

    funder = fields.ObjectField(properties={
        'id': fields.KeywordField(),
        'ror': fields.KeywordField(),
        'name': fields.KeywordField(),
        'approved': fields.BooleanField()
    })

    funder_divisions = fields.ListField(fields.KeywordField())
    program_reference_codes = fields.ListField(fields.KeywordField())
    program_officials = fields.NestedField(
        properties = get_person_properties.__func__())
    other_investigators = fields.NestedField(
        properties = get_person_properties.__func__())
    principal_investigator = fields.ObjectField(properties = get_person_properties.__func__())
    awardee_organization = fields.ObjectField(properties = get_organization_properties.__func__())
    keywords = fields.ListField(fields.KeywordField())

    class Index:
        name = 'grant_index'
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
    
    class Django:
        model = Grant
        related_models = [Funder, Person, Organization]

        fields = [
             'id',
             'award_id',
             'title',
             'start_date',
             'end_date',
             'award_amount',
             'abstract',
             'approved'
         ]

    def prepare_other_investigators(self, instance):

        def prepare_affiliations(self, instance): 
            affiliations = []
            if instance.affiliations.all().count() > 0:
                for affiliation in instance.affiliations.all():
                    affiliations.append({
                        'id': affiliation.id,
                        'ror': affiliation.ror,
                        'name': affiliation.name,
                        'address': affiliation.address,
                        'city': affiliation.city,
                        'state': affiliation.state,
                        'zip': affiliation.zip,
                        'country': affiliation.country,
                        'approved': affiliation.approved
                    })
            return affiliations

        people = []

        if instance.other_investigators.all().count() > 0:
            for person in instance.other_investigators.all():
                people.append(
                    {
                        'id': person.id,
                        'first_name': person.first_name,
                        'last_name': person.last_name,
                        'full_name': person.first_name + ' ' + person.last_name,
                        'orcid': person.orcid,
                        'emails': person.emails,
                        'private_emails': person.private_emails,
                        'keywords': person.keywords,
                        'affiliations': prepare_affiliations(self, person),
                        'approved': person.approved,
                        'websites': person.websites,
                        'desired_collaboration': person.desired_collaboration,
                        'comments': person.comments
                    }
                )
        return people

    def prepare_program_officials(self, instance):

        def prepare_affiliations(self, instance): 
            affiliations = []
            if instance.affiliations.all().count() > 0:
                for affiliation in instance.affiliations.all():
                    affiliations.append({
                        'id': affiliation.id,
                        'ror': affiliation.ror,
                        'name': affiliation.name,
                        'address': affiliation.address,
                        'city': affiliation.city,
                        'state': affiliation.state,
                        'zip': affiliation.zip,
                        'country': affiliation.country,
                        'approved': affiliation.approved
                    })
            return affiliations

        people = []

        if instance.program_officials.all().count() > 0:
            for person in instance.program_officials.all():
                people.append(
                    {
                        'id': person.id,
                        'first_name': person.first_name,
                        'last_name': person.last_name,
                        'full_name': person.first_name + ' ' + person.last_name,
                        'orcid': person.orcid,
                        'emails': person.emails,
                        'private_emails': person.private_emails,
                        'keywords': person.keywords,
                        'affiliations': prepare_affiliations(self, person),
                        'approved': person.approved,
                        'websites': person.websites,
                        'desired_collaboration': person.desired_collaboration,
                        'comments': person.comments
                    }
                )
        return people

    def prepare_principal_investigator(self, instance):
        #pi = {}
        def prepare_affiliations(self, instance): 
            affiliations = []
            if instance.affiliations.all().count() > 0:
                for affiliation in instance.affiliations.all():
                    affiliations.append({
                        'id': affiliation.id,
                        'ror': affiliation.ror,
                        'name': affiliation.name,
                        'address': affiliation.address,
                        'city': affiliation.city,
                        'state': affiliation.state,
                        'zip': affiliation.zip,
                        'country': affiliation.country,
                        'approved': affiliation.approved
                    })
            return affiliations

        if instance.principal_investigator:
            return {
                'id': instance.principal_investigator.id,
                'first_name': instance.principal_investigator.first_name,
                'last_name': instance.principal_investigator.last_name,
                'full_name': instance.principal_investigator.first_name + ' ' + instance.principal_investigator.last_name,
                'orcid': instance.principal_investigator.orcid,
                'emails': instance.principal_investigator.emails,
                'private_emails': instance.principal_investigator.private_emails,
                'keywords': instance.principal_investigator.keywords,
                'affiliations': prepare_affiliations(self, instance.principal_investigator),
                'approved': instance.principal_investigator.approved,
                'websites': instance.principal_investigator.websites,
                'desired_collaboration': instance.principal_investigator.desired_collaboration,
                'comments': instance.principal_investigator.comments
            }
        else:
            return None