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
       
    def prepare_authors(self, instance):
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

    authors = fields.NestedField(
        properties = get_person_properties.__func__())
    # grants = fields.NestedField(
    #     properties = get_grant_properties.__func__())
    keywords = fields.ListField(fields.TextField())

    class Index:
        name = 'publication_index'
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
        auto_refresh = True

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

