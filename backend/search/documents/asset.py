from django_opensearch_dsl.registries import registry
from django_opensearch_dsl import Document, fields
from apis.models import Asset, Person, Grant, Publication, Organization, Dataset


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

@staticmethod
def get_publication_properties():
    return {
        'id': fields.IntegerField(),
        'doi': fields.KeywordField(),
        'title': fields.KeywordField(),
        'authors': fields.NestedField(properties = {
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
        })
    }

@staticmethod
def get_dataset_properties():
    return {
        'id': fields.IntegerField(),
        'doi': fields.KeywordField(),
        'title': fields.KeywordField(),
        'download_path': fields.KeywordField(),
        'size': fields.KeywordField(),
        'mime_type': fields.KeywordField(),
        'approved': fields.BooleanField(),
        'authors': fields.NestedField(properties = {
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
        }),
        'grants': fields.NestedField(properties = {
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
                })
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
        'program_officials': fields.NestedField(properties = {
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
        'principal_investigator': fields.NestedField(properties = {
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
        'other_investigators': fields.NestedField(properties = {
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
        'awardee_organization': fields.NestedField(properties = {
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

@registry.register_document
class AssetDocument(Document):
    
    keywords = fields.ListField(fields.KeywordField())
    organization = fields.ObjectField(properties = get_organization_properties.__func__())
    author = fields.ObjectField(properties = get_person_properties.__func__())
    publication = fields.ObjectField(properties = get_publication_properties.__func__())
    dataset = fields.ObjectField(properties = get_dataset_properties.__func__())
    grant = fields.ObjectField(properties = get_dataset_properties.__func__())

    class Index:
        name = 'asset_index'
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Asset
        related_models = [Person, Organization, Grant, Dataset]

        fields = [
             'id',
             'doi',
             'filename',
             'download_path',
             'size',
             'mime_type',
             'checksum',
             'approved'
        ]