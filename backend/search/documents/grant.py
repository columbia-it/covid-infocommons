from ast import Or
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from apis.models import Grant, Funder, Person, Organization


@registry.register_document
class GrantDocument(Document):
    print("*** GrantDocument **")

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
             'funder'
         ]