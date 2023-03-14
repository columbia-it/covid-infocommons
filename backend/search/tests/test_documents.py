from django.test import TestCase
from search.documents import PublicationDocument
from apis.models import Publication, Grant, Person
from django_opensearch_dsl.registries import registry
from django_opensearch_dsl import Document
from django_opensearch_dsl import fields
from django_opensearch_dsl.exceptions import ModelFieldNotMappedError, RedeclaredFieldError
from django.db import models
from unittest.mock import patch, Mock
from django.test import override_settings


class PublicationDocumentTestCase(TestCase):
    test_fixtures = ["search/tests/cic_test_data.json"]

    def test_model_class_added(self):
        self.assertEqual(PublicationDocument.Django.model, Publication)

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