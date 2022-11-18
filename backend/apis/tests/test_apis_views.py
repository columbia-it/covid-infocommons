from django.test import TestCase
from apis.models import Organization, Person, Funder, Grant
from apis.tests.factories import OrganizationFactory, FunderFactory, GrantFactory
from apis.serializers import GrantSerializer, CreateGrantSerializer
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.request import Request
from apis.views import OrganizationViewSet, GrantViewSet
from rest_framework.exceptions import NotFound

class APIURLsTest(APITestCase):
    def setUp(self) -> None:
        self.person = Person.objects.create(
            first_name='Ida',
            last_name='Rogers',
            orcid='https://orcid.org/0000-0002-1825-0097',
            emails='IdaJRogers@dayrep.com',
        )
        self.org = Organization.objects.create(
            ror='https://ror.org/049wwwm08',
            name='Environmental Development Centre',
            address='1000 Business Center Drive',
            city='San Diego',
            state='CA',
            country='USA',
            zip='32746'
        )
        self.person.affiliations.add(self.org)
        self.person.save()
        return super().setUp()

    def test_root(self):
        response = self.client.get('/v1/')
        self.assertEqual(response.status_code, 200)

    def test_org_link(self):
        response = self.client.get('/v1/organizations')
        self.assertEqual(response.status_code, 200)

    def test_people_link(self):
        response = self.client.get('/v1/people')
        self.assertEqual(response.status_code, 200)

    def test_grants_link(self):
        response = self.client.get('/v1/grants')
        self.assertEqual(response.status_code, 200)

    def test_publications_link(self):
        response = self.client.get('/v1/publications')
        self.assertEqual(response.status_code, 200)

    def test_datasets_link(self):
        response = self.client.get('/v1/datasets')
        self.assertEqual(response.status_code, 200)

    def test_assets_link(self):
        response = self.client.get('/v1/assets')
        self.assertEqual(response.status_code, 200)

    def test_get_person_affiliations(self):
        self.assertEqual(self.person.affiliations.count(), 1)

class APIViewTest(APITestCase):
    def setUp(self) -> None:
        self.grant = GrantFactory()
        return super().setUp()

    def test_grant_viewset(self):
        response = self.client.get('/v1/grants', {"page[number]": 1})
        self.assertEqual(response.status_code, 200)
        expected = {
            'links': {
                'first': 'http://testserver/v1/grants?page%5Bnumber%5D=1', 
                'last': 'http://testserver/v1/grants?page%5Bnumber%5D=1', 
                'next': None, 
                'prev': None
            }, 
            'data': [{
                'type': 'Grant', 
                'id': '1', 
                'attributes': {
                    'award_id': self.grant.award_id, 
                    'title': self.grant.title, 
                    'funder': {
                        'id': self.grant.funder.id, 
                        'ror': self.grant.funder.ror, 
                        'name': self.grant.funder.name, 
                        'approved': self.grant.funder.approved
                    }, 
                    'funder_divisions': self.grant.funder_divisions, 
                    'program_reference_codes': [], 
                    'program_officials': [], 
                    'start_date': None, 
                    'end_date': None, 
                    'award_amount': None, 
                    'principal_investigator': None, 
                    'other_investigators': [], 
                    'awardee_organization': None, 
                    'abstract': None, 
                    'keywords': None, 
                    'approved': True
                }
            }], 
            'meta': {
                'pagination': {
                'page': 1, 
                'pages': 1, 
                'count': 1
                    }
                }
            }
        
        assert expected == response.json()


class TestGrantViewMixin(APITestCase):
    def setUp(self) -> None:
        self.organization = OrganizationFactory()
        self.funder = FunderFactory()
        self.grant = GrantFactory()
        self.grant.funder = self.funder

    def _get_view(self, kwargs, action='get'):
        factory = APIRequestFactory()
        request = Request(factory.get("", content_type="application/vnd.api+json"))
        return GrantViewSet(request=request, kwargs=kwargs, action=action)

    # def test_get_related_field_name(self):
    #     kwargs = {'pk': self.organization.id, 'related_field': 'ror'}
    #     view = self._get_view(kwargs)
    #     print('====')
    #     got = view.get_related_field_name()
    #     print('..2..')
    #     print(got)
    #     self.assertEqual(got, kwargs["related_field"])

    def test_get_related_instance_model_field(self):
        kwargs = {"pk": self.grant.id, "related_field": "funder"}
        view = self._get_view(kwargs)
        got = view.get_related_instance()
        self.assertTrue(type(got), Funder)
        self.assertEqual(self.grant.funder.id, self.funder.id)

    def test_get_create_serializer_class(self):
        kwargs = {"action": "create", "pk": self.grant.id, "related_field": "funder"}
        view = self._get_view(kwargs, 'create')
        got = view.get_serializer_class()
        self.assertEqual(got, CreateGrantSerializer)

    def test_get_default_serializer_class(self):
        kwargs = {"pk": self.grant.id, "related_field": "funder"}
        view = self._get_view(kwargs)
        got = view.get_serializer_class()
        self.assertEqual(got, GrantSerializer)

class TestValidationErrorResponses(APITestCase):
    pass


        