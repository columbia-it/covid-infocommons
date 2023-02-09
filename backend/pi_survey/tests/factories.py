import factory
from faker import Factory as FakerFactory
from pi_survey.models import Survey
from faker.providers.person import Provider

faker = FakerFactory.create()
import random

class SurveyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Survey

    id = str(faker.random_number(digits=7))
    first_name = faker.first_name()
    last_name = faker.last_name()
    orcid = faker.url()
    award_id = random.randint(2200000, 2222000)
    funder_name = random.choice(['NSF', 'NIH', 'NA', 'Other'])
    grant_keywords = '{kw1}{kw2}'.format(kw1=faker.word(), kw2=faker.word())
    email = faker.email()
    person_additional_comments = faker.sentence(nb_words=200)
    desired_collaboration = faker.sentence(nb_words=200)
    dois = faker.sentence(nb_words=200)
    grant_additional_keywords = '{kw1}{kw2}'.format(kw1=faker.word(), kw2=faker.word())
    is_copi = False
    websites = "{website1},{website2}".format(website1=faker.uri(), website2=faker.uri())
