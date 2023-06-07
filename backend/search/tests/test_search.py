from ast import alias
from django.test import TestCase
from django_opensearch_dsl.registries import registry
from search.documents import PublicationDocument
from apis.models import Publication
from opensearchpy import OpenSearch
from opensearch_dsl.connections import connections


class PublicationSearchTestCase(TestCase):
    fixtures = ["search/tests/cic_test_data.json"]
    
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

        # client = OpenSearch(
        #     hosts = [{"host": "localhost", "port": 9200}],
        #     http_auth = ("admin", "admin"),
        #     use_ssl = True,
        #     verify_certs = False,
        #     ssl_assert_hostname = False,
        #     ssl_show_warn = False,
        # )
        #print(client.info())
        # indices = registry.get_indices()
        # for i in indices:
        #     i.delete(ignore_unavailable=True)

    def tearDown(self) -> None:
        PublicationDocument._index.delete()
        return super().tearDown()

    def test_search_publication(self):
        PublicationDocument._index.create()
        PublicationDocument().update(PublicationDocument().get_indexing_queryset(), "index", refresh=True)

        self.assertEqual(
            set(PublicationDocument.search().query("term", **{"title": "test"}).extra(size=300).to_queryset()),
            set(Publication.objects.filter(title="test")),
        )

    def test_search_publication_cache(self):
        PublicationDocument._index.create()
        PublicationDocument().update(PublicationDocument().get_indexing_queryset(), "index", refresh=True)
        search = PublicationDocument.search().query("term", **{"title": "test"}).extra(size=300)
        search.execute()
        self.assertEqual(
            set(search.to_queryset(keep_order=True)), set(Publication.objects.filter(title="test"))
        )

    def test_search_country_keep_order(self):
        PublicationDocument._index.create()

        PublicationDocument().update(PublicationDocument().get_indexing_queryset(), "index", refresh=True)
        search = PublicationDocument.search().query("term", **{"title": "test"}).extra(size=300)
        self.assertEqual(
            set(search.to_queryset(keep_order=True)), set(Publication.objects.filter(title="test"))
        )