from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from apis.models import Person, Organization


@registry.register_document
class PersonDocument(Document):

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

    affiliations = fields.NestedField(
        properties = get_organization_properties.__func__())
    keywords = fields.ListField(fields.TextField())
    websites = fields.ListField(fields.TextField())
    full_name = fields.TextField()

    class Index:
        name = 'person_index'
        settings = {"number_of_shards": 2, "number_of_replicas": 0}
        auto_refresh = True
    
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
             'desired_collaboration',
             'comments',
             'approved'
        ]
    
    def prepare_full_name(self, instance):
        return instance.first_name + ' ' + instance.last_name

