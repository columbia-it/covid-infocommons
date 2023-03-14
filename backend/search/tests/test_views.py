from django.test import TestCase, RequestFactory, Client
from unittest.mock import patch
from opensearchpy.client import OpenSearch


class SearchViewTest(TestCase):
    test_fixtures = ["search/tests/cic_test_data.json"]
    
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def fake_facet_search(self, body, index):
        search_result = {
            "took": 5, 
            "timed_out": False, 
            "_shards": {
                "total": 1, 
                "successful": 1, 
                "skipped": 0, 
                "failed": 0
            }, 
            "hits": {
                "total": {
                    "value": 0, 
                    "relation": "eq"
                }, 
                "max_score": None, 
                "hits": []
            }, 
            "aggregations": {
                "patterns": {
                    "doc_count_error_upper_bound": 0, 
                    "sum_other_doc_count": 0, 
                    "buckets": [
                        {"key": "A. Cymene Howe", "doc_count": 1},
                        {"key": "ADARBAD MASTER", "doc_count": 2}, 
                        {"key": "ADOLFO GARCIA-SASTRE", "doc_count": 2},
                         {"key": "ADRIANA GRUPPI", "doc_count": 1}, 
                         {"key": "ADRIENNE SARAH JUARASCIO", "doc_count": 2}, 
                         {"key": "AHAMED H IDRIS", "doc_count": 1}, 
                         {"key": "AKSHAY SOOD", "doc_count": 2}, 
                         {"key": "ALAN L. MENDELSOHN", "doc_count": 3}]
                }
            }
        }
        return search_result

    @patch.object(OpenSearch, 'search', fake_facet_search)
    def test_get_facet_by_field(self):
        response = self.client.get('/search/facets?field=principal_investigator.full_name')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get('content-type'), 'application/json')

    def fake_grant_search(self, body, index):
        search_result = {
            "took": 38, "timed_out": False, 
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0}, 
            "hits": {
                "total": {"value": 7, "relation": "eq"}, 
                "max_score": None, "hits": [
                    {
                        "_index": "grant_index", "_type": "_doc", 
                        "_id": "1171", "_score": 11.878323, 
                        "_source": {
                            "funder": {"id": 3, "ror": "https://ror.org/021nxhr62", "name": "National Science Foundation", "approved": True}, 
                            "funder_divisions": ["Engineering (ENG)"], "program_reference_codes": [], 
                            "program_officials": [{"emails": "", "full_name": "Elizabeth Blood", "keywords": None, "last_name": "Blood", "affiliations": [], "orcid": None, "id": 2975, "first_name": "Elizabeth", "private_emails": ""}], 
                            "other_investigators": [{"id": 2976, "first_name": "Winslow D", "last_name": "Hansen", "orcid": None, "emails": "", "private_emails": "", "keywords": None, "affiliations": []}], 
                            "principal_investigator": {"id": 2977, "first_name": "Steward T", "last_name": "Pickett", "orcid": None, "emails": "picketts@caryinstitute.org", "private_emails": "https://covidinfocommons.datascience.columbia.edu/content/steward-t-pickett", "keywords": None, "affiliations": [], "full_name": "Steward T Pickett", "approved": True}, 
                            "awardee_organization": {"id": 536, "ror": "", "name": "Cary Institute of Ecosystem Studies, Inc.", "address": "", "city": "", "state": "NY", "zip": "", "country": "United States", "approved": True}, 
                            "keywords": [], "id": 1171, "award_id": "2115414", 
                            "title": "SRS-RN: The Continuum of Urbanity as an Organizing Concept to Promote Sustainability in the Mid-Hudson Region", "start_date": "2021-11-01", "end_date": "2022-10-31", "award_amount": 150000, "abstract": "Learning how people can sustainably live in a world where urban sign firms, and government agencies", "approved": True}, "sort": [11.878323, 1635724800000]
                    }, 
                    {
                        "_index": "grant_index", "_type": "_doc", "_id": "4290", "_score": 8.959292, 
                        "_source": {"funder": {"id": 3, "ror": "https://ror.org/021nxhr62", "name": "National Science Foundation", "approved": True}, "funder_divisions": ["Unknown", "NSF INCLUDES"], "program_reference_codes": [], "program_officials": [], "other_investigators": [{"id": 14557, "first_name": "Einat", "last_name": "Lev", "orcid": None, "emails": "", "private_emails": "", "keywords": None, "affiliations": []}, {"id": 14558, "first_name": "Matthew", "last_name": "Palmer", "orcid": None, "emails": "", "private_emails": "", "keywords": None, "affiliations": []}, {"id": 14559, "first_name": "Margie", "last_name": "Turrin", "orcid": None, "emails": "", "private_emails": "", "keywords": None, "affiliations": []}, {"id": 14560, "first_name": "Luo Cassie", "last_name": "Xu", "orcid": None, "emails": "", "private_emails": "", "keywords": None, "affiliations": []}], "principal_investigator": {"id": 14561, "first_name": "Robert", "last_name": "Newton", "orcid": None, "emails": "", "private_emails": "", "keywords": None, "affiliations": [], "full_name": "Robert Newton", "approved": True}, "awardee_organization": {"id": 196, "ror": "https://ror.org/00hj8s172", "name": "Columbia University", "address": "", "city": "", "state": "NY", "zip": "", "country": "United States", "approved": True}, "keywords": [], "id": 4290, "award_id": "1649310", "title": "NSF INCLUDES:  Early Engagement in Research: key to STEM retention", "start_date": "2016-10-01", "end_date": "2021-09-30", "award_amount": 299995}
                    }
                ]
            }
        }
        return search_result
    
    @patch.object(OpenSearch, 'search', fake_grant_search)
    def test_search_grants_by_keyword(self):
        response = self.client.get('/search/grants?keyword=Pickett')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get('content-type'), 'application/json')
        self.assertIsNotNone(response.json)

    @patch.object(OpenSearch, 'search', fake_grant_search)
    def test_search_grants_by_filter(self):
        response = self.client.get('/search/grants?from=0&org_state=CA&funder_name=National+Institutes+of+Health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get('content-type'), 'application/json')
        self.assertIsNotNone(response.json)


