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
        }

    @staticmethod
    def get_person_properties():
        return {
            'id': fields.IntegerField(),
            'first_name': fields.KeywordField(),
            'last_name': fields.KeywordField(),
            'orcid': fields.KeywordField(),
            'emails': fields.KeywordField(),
            'private_emails': fields.KeywordField(),
            'keywords': fields.KeywordField(),
            'affiliations': fields.NestedField(properties = {
                'id': fields.IntegerField(),
                'ror': fields.KeywordField(),
                'name': fields.KeywordField(),
                'address': fields.KeywordField(),
                'city': fields.KeywordField(),
                'state': fields.KeywordField(),
                'zip': fields.KeywordField(),
                'country': fields.KeywordField()
            })
        }

    funder = fields.ObjectField(properties={
        'id': fields.KeywordField(),
        'ror': fields.KeywordField(),
        'name': fields.KeywordField()
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
             'abstract'
         ]