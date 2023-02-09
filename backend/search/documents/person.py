from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from apis.models import Person, Organization

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

@registry.register_document
class PersonDocument(Document):
    keywords = fields.ListField(fields.TextField())
    affiliations = fields.NestedField(
        properties = get_organization_properties.__func__())
        
    class Index:
        name = 'person_index'
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Person
        related_models = [Organization]

        fields = [
             'id',
             'first_name',
             'last_name',
             'orcid',
             'emails',
             'private_emails',
             'websites',
             'approved',
             'desired_collaboration',
             'comments'
         ]

