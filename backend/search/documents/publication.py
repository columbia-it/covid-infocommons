from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from apis.models import Publication, Person, Grant

@registry.register_document
class PublicationDocument(Document):

    @staticmethod
    def get_organization_properties():
        return {
            'id': fields.IntegerField(),
            'ror': fields.TextField(),
            'name': fields.TextField(),
            'address': fields.TextField(),
            'city': fields.TextField(),
            'state': fields.TextField(),
            'zip': fields.TextField(),
            'country': fields.TextField(),
            'approved': fields.BooleanField()
        }

    @staticmethod
    def get_person_properties():
        return {
            'id': fields.IntegerField(),
            'first_name': fields.TextField(),
            'last_name': fields.TextField(),
            'full_name': fields.TextField(),
            'orcid': fields.TextField(),
            'emails': fields.TextField(),
            'private_emails': fields.TextField(),
            'keywords': fields.TextField(),
            'full_name': fields.TextField(),
            'approved': fields.BooleanField(),
            'websites': fields.TextField(),
            'desired_collaboration': fields.TextField(),
            'comments': fields.TextField(),
            'affiliations': fields.NestedField(properties = {
                'id': fields.IntegerField(),
                'ror': fields.TextField(),
                'name': fields.TextField(),
                'address': fields.TextField(),
                'city': fields.TextField(),
                'state': fields.TextField(),
                'zip': fields.TextField(),
                'country': fields.TextField(),
                'approved': fields.BooleanField()
            })
        }

    @staticmethod
    def get_grant_properties():
        return {
            'id': fields.IntegerField(),
            'award_id': fields.TextField(),
            'title': fields.TextField(),
            'funder': fields.NestedField(properties = {
                'id': fields.IntegerField(),
                'ror': fields.TextField(),
                'name': fields.TextField(),
                'approved': fields.BooleanField()
            }),
            'funder_divisions': fields.TextField(),
            'program_reference_codes': fields.TextField(),
            'program_officials': fields.NestedField(
                properties = {
                    'id': fields.IntegerField(),
                    'first_name': fields.TextField(),
                    'last_name': fields.TextField(),
                    'full_name': fields.TextField(),
                    'orcid': fields.TextField(),
                    'emails': fields.TextField(),
                    'private_emails': fields.TextField(),
                    'keywords': fields.TextField(),
                    'full_name': fields.TextField(),
                    'approved': fields.BooleanField(),
                    'websites': fields.TextField(),
                    'desired_collaboration': fields.TextField(),
                    'comments': fields.TextField(),
                    'affiliations': fields.NestedField(properties = {
                        'id': fields.IntegerField(),
                        'ror': fields.TextField(),
                        'name': fields.TextField(),
                        'address': fields.TextField(),
                        'city': fields.TextField(),
                        'state': fields.TextField(),
                        'zip': fields.TextField(),
                        'country': fields.TextField(),
                        'approved': fields.BooleanField()
                    })
                }),
            'start_date': fields.DateField(),
            'end_date': fields.DateField(),
            'award_amount': fields.IntegerField(),
            'principal_investigator': fields.NestedField(
                properties = {
                    'id': fields.IntegerField(),
                    'first_name': fields.TextField(),
                    'last_name': fields.TextField(),
                    'full_name': fields.TextField(),
                    'orcid': fields.TextField(),
                    'emails': fields.TextField(),
                    'private_emails': fields.TextField(),
                    'keywords': fields.TextField(),
                    'full_name': fields.TextField(),
                    'approved': fields.BooleanField(),
                    'websites': fields.TextField(),
                    'desired_collaboration': fields.TextField(),
                    'comments': fields.TextField(),
                    'affiliations': fields.NestedField(properties = {
                        'id': fields.IntegerField(),
                        'ror': fields.TextField(),
                        'name': fields.TextField(),
                        'address': fields.TextField(),
                        'city': fields.TextField(),
                        'state': fields.TextField(),
                        'zip': fields.TextField(),
                        'country': fields.TextField(),
                        'approved': fields.BooleanField()
                    })
                }),
            'other_investigators': fields.NestedField(
                properties = {
                    'id': fields.IntegerField(),
                    'first_name': fields.TextField(),
                    'last_name': fields.TextField(),
                    'full_name': fields.TextField(),
                    'orcid': fields.TextField(),
                    'emails': fields.TextField(),
                    'private_emails': fields.TextField(),
                    'keywords': fields.TextField(),
                    'full_name': fields.TextField(),
                    'approved': fields.BooleanField(),
                    'websites': fields.TextField(),
                    'desired_collaboration': fields.TextField(),
                    'comments': fields.TextField(),
                    'affiliations': fields.NestedField(properties = {
                        'id': fields.IntegerField(),
                        'ror': fields.TextField(),
                        'name': fields.TextField(),
                        'address': fields.TextField(),
                        'city': fields.TextField(),
                        'state': fields.TextField(),
                        'zip': fields.TextField(),
                        'country': fields.TextField(),
                        'approved': fields.BooleanField()
                    })
                }),
            'awardee_organization': fields.NestedField(
                properties = {
                    'id': fields.IntegerField(),
                    'ror': fields.TextField(),
                    'name': fields.TextField(),
                    'address': fields.TextField(),
                    'city': fields.TextField(),
                    'state': fields.TextField(),
                    'zip': fields.TextField(),
                    'country': fields.TextField(),
                    'approved': fields.BooleanField()
                }),
            'abstract': fields.TextField(),
            'keywords': fields.TextField(),
            'approved': fields.BooleanField()
        }
    
    def prepare_grants(self, instance):
        def prepare_funder(self, instance):
            if instance.funder:
                return {
                    'id': instance.funder.id,
                    'ror': instance.funder.ror,
                    'name': instance.funder.name,
                    'approved': instance.funder.approved
                }

        def prepare_program_officials(self, instance):
            people = []
            if instance.program_officials.all().count() > 0:
                people = []
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

        def prepare_principal_investigator(self, instance):
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
        def prepare_other_investigators(self, instance):
            people = []
            if instance.other_investigators.all().count() > 0:
                people = []
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

        def prepare_awardee_organization(self, instance):
            if instance:
                return {
                    'id': instance.id,
                    'ror': instance.ror,
                    'name': instance.name,
                    'address': instance.address,
                    'city': instance.city,
                    'state': instance.state,
                    'zip': instance.zip,
                    'country': instance.country,
                    'approved': instance.approved
                }

        grants = []
        if instance.grants.all().count() > 0:
            for grant in instance.grants.all():
                grants.append(
                    {
                    'id': grant.id,
                    'award_id': grant.award_id,
                    'title': grant.title,
                    'funder': prepare_funder(self, grant),
                    'funder_divisions': grant.funder_divisions,
                    'program_reference_codes': grant.program_reference_codes,
                    'program_officials': prepare_program_officials(self, grant),
                    'start_date': grant.start_date,
                    'end_date': grant.end_date,
                    'award_amount': grant.award_amount,
                    'principal_investigator': prepare_principal_investigator(self, grant),
                    'other_investigators': prepare_other_investigators(self, grant),
                    'awardee_organization': prepare_awardee_organization(self, grant.awardee_organization),
                    'abstract': grant.abstract,
                    'keywords': grant.keywords,
                    'approved': grant.approved
                    }
                )
                return grants
       
    def prepare_authors(self, instance):
        print('......prepare_authors().....')
        def prepare_affiliations(self, instance): 
            print('......prepare_affiliations().....')
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

        if instance.authors.all().count() > 0:
            people = []
            for person in instance.authors.all():
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

    authors = fields.ObjectField(
        properties = get_person_properties.__func__())
    grants = fields.NestedField(
        properties = get_grant_properties.__func__())
    keywords = fields.ListField(fields.TextField())

    class Index:
        name = 'publication_index'
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Publication
        related_models = [Grant, Person]

        fields = [
             'id',
             'doi',
             'title',
             'issn',
             'language',
             'publication_date',
             'publication_type',
             'approved'
         ]

