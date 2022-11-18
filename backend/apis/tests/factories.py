import factory
from faker import Factory as FakerFactory
from apis.models import Funder, Organization, Grant

faker = FakerFactory.create()

class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    ror = factory.LazyAttribute(lambda x: faker.name())
    name = faker.company()

class FunderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Funder

    ror = factory.LazyAttribute(lambda x: faker.name())
    name = factory.LazyAttribute(lambda x: faker.name())

class GrantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Grant

    award_id = str(faker.random_number(digits=7))
    title = faker.sentence()
    funder = factory.SubFactory(FunderFactory)
    funder_divisions = []
    for _ in range(3):
        funder_divisions.append(faker.word())



