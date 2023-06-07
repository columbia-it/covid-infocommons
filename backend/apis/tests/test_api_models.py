from django.test import TestCase
from apis.models import Person, Organization

class APIModelsTest(TestCase):

    def setUp(self) -> None:
        Person.objects.create(
            first_name='sam', 
            last_name='smith', 
            orcid='0000-0002-1825-0097',
            websites=[])
        Organization.objects.create(
            ror='https://ror.org/049wwwm08',
            name='Environmental Development Centre',
            address='1000 Business Center Drive',
            city='San Diego',
            state='CA',
            country='USA',
            zip='32746'
        )
        return super().setUp()

    def test_person_name(self):
        person = Person.objects.get(first_name='sam')
        self.assertEqual(person.last_name, 'smith')

    def test_orcid_max_length(self):
        person = Person.objects.get(first_name='sam')
        max_length = person._meta.get_field('orcid').max_length
        self.assertEqual(max_length, 1000)

    def test_websites_max_length(self):
        person = Person.objects.get(first_name='sam')
        person.websites.append('https://nsf.gov/awardsearch/showAward?AWD_ID=2116631&HistoricalAwards=false')
        person.save()
        websites = person._meta.get_field('websites')
        self.assertEqual(websites.max_length, 1000)
        self.assertEqual(len(person.websites), 1)

    def test_affiliations(self):
        person = Person.objects.get(first_name='sam')
        organization = Organization.objects.get(id=1)
        person.affiliations.add(organization)
        person.save()
