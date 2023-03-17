from django.test import TestCase
from search.documents import PublicationDocument, GrantDocument, PersonDocument
from apis.models import Publication, Grant, Person, Organization, Funder
from django_opensearch_dsl.registries import registry
from django_opensearch_dsl import Document
from django_opensearch_dsl import fields
from django_opensearch_dsl.exceptions import ModelFieldNotMappedError, RedeclaredFieldError
from django.db import models
from unittest.mock import patch, Mock
from django.test import override_settings
from opensearch_dsl.connections import connections


class PublicationDocumentTest(TestCase):
    test_fixtures = ["search/tests/cic_test_data.json"]

    def test_model_class_added(self):
        self.assertEqual(PublicationDocument.Django.model, Publication)

    def test_auto_refresh_default(self):
        self.assertTrue(PublicationDocument.Index.auto_refresh)

    def test_auto_refresh_default(self):
        self.assertTrue(PublicationDocument.Index.auto_refresh)

    def test_auto_refresh_added(self):
        @registry.register_document
        class PublicationDocument2(Document):
            class Django:
                model = Publication
            
            class Index:
                auto_refresh = False

        self.assertFalse(PublicationDocument2.Index.auto_refresh)

    def test_fields_populated(self):
        mapping = PublicationDocument._doc_type.mapping
        self.assertEqual(set(mapping.properties.properties.to_dict().keys()), 
            {'id', 'doi', 'title', 'issn', 'language', 'publication_date', 'publication_type', 'approved', 'authors', 'keywords'})
    
    def test_related_models_added(self):
        related_models = PublicationDocument.Django.related_models
        self.assertEqual([Grant, Person], related_models)

    def test_to_field(self):
        doc = Document()
        titleField = doc.to_field("title", Publication._meta.get_field("title"))
        self.assertIsInstance(titleField, fields.TextField)
        self.assertEqual(titleField._path, ["title"])
        
        doiField = doc.to_field("doi", Publication._meta.get_field("doi"))
        self.assertIsInstance(doiField, fields.TextField)
        self.assertEqual(doiField._path, ["doi"])
        
        issnField = doc.to_field("issn", Publication._meta.get_field("issn"))
        self.assertIsInstance(issnField, fields.TextField)
        self.assertEqual(issnField._path, ["issn"])

        languageField = doc.to_field("language", Publication._meta.get_field("language"))
        self.assertIsInstance(languageField, fields.TextField)
        self.assertEqual(languageField._path, ["language"])

        publicationDateField = doc.to_field("publication_date", Publication._meta.get_field("publication_date"))
        self.assertIsInstance(publicationDateField, fields.DateField)
        self.assertEqual(publicationDateField._path, ["publication_date"])

        publicationTypeField = doc.to_field("publication_type", Publication._meta.get_field("publication_type"))
        self.assertIsInstance(publicationTypeField, fields.TextField)
        self.assertEqual(publicationTypeField._path, ["publication_type"])

        approvedField = doc.to_field("approved", Publication._meta.get_field("approved"))
        self.assertIsInstance(approvedField, fields.BooleanField)
        self.assertEqual(approvedField._path, ["approved"])

    def test_to_field_with_unknown_field(self):
        doc = Document()
        with self.assertRaises(ModelFieldNotMappedError):
            doc.to_field("grants", Publication._meta.get_field("grants"))

    def test_get_queryset(self):
        qs = PublicationDocument().get_queryset()
        self.assertIsInstance(qs, models.QuerySet)
        self.assertEqual(qs.model, Publication)


class GrantDocumentTest(TestCase):
    test_fixtures = ["search/tests/cic_test_data.json"]

    def setUp(self) -> None:
        conn = connections.create_connection(
            hosts=[{
                "host": "localhost", 
                "port": 9200,
                "http_auth": ("admin", "admin"),
                "use_ssl": True,
                "verify_certs": False,
            }], 
            alias='default')
        connections.configure(
                default={
                    'hosts': 'localhost', 
                    'port': 9200,
                    "http_auth": ("admin", "admin"),
                    "use_ssl": True,
                    "verify_certs": False,
                },
        )
    
    def tearDown(self) -> None:
        GrantDocument._index.delete()
        return super().tearDown()

    def test_model_class_added(self):
        GrantDocument._index.create()
        self.assertEqual(GrantDocument.Django.model, Grant)

    def test_fields_populated(self):
        GrantDocument._index.create()
        mapping = GrantDocument._doc_type.mapping
        self.assertEqual(set(mapping.properties.properties.to_dict().keys()), 
            {'id', 'award_id', 'title', 'start_date', 'end_date', 'award_amount', 'abstract', 'approved', 'funder', 'funder_divisions', 'program_reference_codes', 'program_officials', 'other_investigators', 'principal_investigator', 'awardee_organization', 'keywords'})
    
    def test_related_models_added(self):
        GrantDocument._index.create()
        related_models = GrantDocument.Django.related_models
        self.assertEqual([Funder, Person, Organization], related_models)

    def test_to_field(self):
        GrantDocument._index.create()
        doc = Document()
        titleField = doc.to_field("title", Grant._meta.get_field("title"))
        self.assertIsInstance(titleField, fields.TextField)
        self.assertEqual(titleField._path, ["title"])
        
        awardIdField = doc.to_field("award_id", Grant._meta.get_field("award_id"))
        self.assertIsInstance(awardIdField, fields.TextField)
        self.assertEqual(awardIdField._path, ["award_id"])
        
        awardAmountField = doc.to_field("award_amount", Grant._meta.get_field("award_amount"))
        self.assertIsInstance(awardAmountField, fields.IntegerField)
        self.assertEqual(awardAmountField._path, ["award_amount"])

        startDateField = doc.to_field("start_date", Grant._meta.get_field("start_date"))
        self.assertIsInstance(startDateField, fields.DateField)
        self.assertEqual(startDateField._path, ["start_date"])

        approvedField = doc.to_field("approved", Grant._meta.get_field("approved"))
        self.assertIsInstance(approvedField, fields.BooleanField)
        self.assertEqual(approvedField._path, ["approved"])

    def test_to_field_with_unknown_field(self):
        GrantDocument._index.create()
        doc = Document()
        with self.assertRaises(ModelFieldNotMappedError):
            doc.to_field("doi", Grant._meta.get_field("funder"))

    def test_get_queryset(self):
        GrantDocument._index.create()
        qs = GrantDocument().get_queryset()
        self.assertIsInstance(qs, models.QuerySet)
        self.assertEqual(qs.model, Grant)

    def test_model_instance_update_refresh_true(self):
        GrantDocument._index.create()
        doc = GrantDocument()
        doc.Index.auto_refresh = False
        grant = Grant()
        with patch("django_opensearch_dsl.documents.bulk") as mock:
            doc.update(grant, "index", refresh=True)
            self.assertEqual(mock.call_args_list[0][1]["refresh"], True)


class PersonDocumentTest(TestCase):
    test_fixtures = ["search/tests/cic_test_data.json"]

    def setUp(self) -> None:
        conn = connections.create_connection(
            hosts=[{
                "host": "localhost", 
                "port": 9200,
                "http_auth": ("admin", "admin"),
                "use_ssl": True,
                "verify_certs": False,
            }], 
            alias='default')
        connections.configure(
                default={
                    'hosts': 'localhost', 
                    'port': 9200,
                    "http_auth": ("admin", "admin"),
                    "use_ssl": True,
                    "verify_certs": False,
                },
        )
        PersonDocument._index.create()

    
    def tearDown(self) -> None:
        PersonDocument._index.delete()
        return super().tearDown()

    def test_model_class_added(self):
        self.assertEqual(PersonDocument.Django.model, Person)

    def test_auto_refresh_default(self):
        self.assertTrue(PersonDocument.Index.auto_refresh)

    def test_auto_refresh_added(self):

        @registry.register_document
        class PersonDocument2(Document):
            
            class Django:
                model = Person

            class Index:
                auto_refresh = False

        self.assertFalse(PersonDocument2.Index.auto_refresh)

    def test_queryset_pagination_added(self):

        @registry.register_document
        class PersonDocument2(Document):
            class Django:
                model = Person
                queryset_pagination = 120

        self.assertEqual(PersonDocument2.django.queryset_pagination, 120)

    def test_fields_populated(self):
        mapping = PersonDocument._doc_type.mapping
        self.assertEqual(set(mapping.properties.properties.to_dict().keys()), {'id','first_name','last_name','orcid','emails','private_emails','desired_collaboration','comments','approved', 'affiliations', 'keywords', 'websites'})

    def test_related_models_added(self):
        related_models = PersonDocument.Django.related_models
        self.assertEqual([Organization], related_models)

    def test_to_field(self):
        doc = Document()
        nameField = doc.to_field("first_name", Person._meta.get_field("first_name"))
        self.assertIsInstance(nameField, fields.TextField)
        self.assertEqual(nameField._path, ["first_name"])

    def test_to_field_with_unknown_field(self):
        doc = Document()
        with self.assertRaises(ModelFieldNotMappedError):
            doc.to_field("award_id", Person._meta.get_field("affiliations"))

    def test_mapping(self):
        self.assertEqual(
            PersonDocument._doc_type.mapping.to_dict(),
            {'properties': {
                'affiliations': {
                    'properties': {
                        'id': {'type': 'integer'}, 
                        'ror': {'type': 'keyword'}, 
                        'name': {'type': 'keyword'}, 
                        'address': {'type': 'keyword'}, 
                        'city': {'type': 'keyword'}, 
                        'state': {'type': 'keyword'}, 
                        'zip': {'type': 'keyword'}, 
                        'country': {'type': 'keyword'}, 
                        'approved': {'type': 'boolean'}
                    }, 
                    'type': 'nested'
                }, 
                'keywords': {'type': 'keyword'}, 
                'websites': {'type': 'keyword'}, 
                'id': {'type': 'long'}, 
                'first_name': {'type': 'text'}, 
                'last_name': {'type': 'text'}, 
                'orcid': {'type': 'text'}, 
                'emails': {'type': 'text'}, 
                'private_emails': {'type': 'text'}, 
                'desired_collaboration': {'type': 'text'}, 
                'comments': {'type': 'text'}, 
                'approved': {'type': 'boolean'}
            }
        }
        )

    def test_get_queryset(self):
        qs = PersonDocument().get_queryset()
        self.assertIsInstance(qs, models.QuerySet)
        self.assertEqual(qs.model, Person)

    def test_get_indexing_queryset(self):
        doc = PersonDocument()
        unordered_qs = doc.get_queryset().order_by("?")

        with patch("django_opensearch_dsl.documents.Document.get_queryset") as mock_qs:
            mock_qs.return_value = unordered_qs
            ordered_continents = list(doc.get_queryset().order_by("id"))
            indexing_continents = list(doc.get_indexing_queryset())
            self.assertEqual(ordered_continents, indexing_continents)
