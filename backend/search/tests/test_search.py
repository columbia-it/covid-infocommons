from django.test import TestCase
from django_opensearch_dsl.registries import registry
from search.documents import PublicationDocument
from apis.models import Publication


class PublicationSearchTestCase(TestCase):
    fixtures = ["search/tests/cic_test_data.json"]

    def setUp(self) -> None:
        indices = registry.get_indices()
        for i in indices:
            i.delete(ignore_unavailable=True)

    def test_search_publication(self):
        PublicationDocument._index.create()

        PublicationDocument().update(PublicationDocument().get_indexing_queryset(), "index", refresh=True)
        self.assertEqual(
            set(PublicationDocument.search().query("term", **{"title": "test"}).extra(size=300).to_queryset()),
            set(Publication.objects.filter(tite="test")),
        )