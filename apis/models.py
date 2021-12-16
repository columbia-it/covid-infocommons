from django.db import models
from django.contrib.postgres.fields import ArrayField


class Organization(models.Model):
    """
    Represents Organization table in the DB
    """
    id = models.IntegerField(primary_key=True)
    ror = models.CharField(max_length=1000, blank=True)
    name = models.CharField(max_length=1000, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=1000, blank=True)
    state = models.CharField(max_length=1000, blank=True)
    zip = models.CharField(max_length=1000, blank=True)
    country = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organization'


class Person(models.Model):
    """
    Represents Person table in the DB
    """
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    orcid = models.CharField(max_length=255, null=True, blank=True)
    emails = models.TextField(null=True, blank=True)
    private_emails = models.CharField(max_length=255, null=True, blank=True)
    keywords = ArrayField(models.CharField(max_length=255, null=True, blank=True), null=True, blank=True)
    affiliations = models.ManyToManyField(Organization, blank=True)

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)

    class Meta:
        db_table = 'person'


class Funder(models.Model):
    """
    Represents Funder table in the DB
    """
    id = models.IntegerField(primary_key=True)
    ror = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'funder'


class Grant(models.Model):
    """
    Represents Grant table in the DB
    """
    id = models.IntegerField(primary_key=True)
    award_id = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    funder = models.ForeignKey(Funder, on_delete=models.CASCADE, db_column='funder', null=True, blank=True)
    funder_divisions = ArrayField(base_field=models.CharField(max_length=200, null=True, blank=True), default=list, blank=True)
    program_reference_codes = ArrayField(base_field=models.CharField(max_length=200, null=True, blank=True), default=list, blank=True)
    program_officials = models.ManyToManyField(Person, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    award_amount = models.IntegerField(null=True, blank=True)
    principal_investigator = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True, related_name='grant_pi')
    other_investigators = models.ManyToManyField(Person, blank=True, related_name='grant_other_investigators')
    awardee_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    keywords = ArrayField(base_field=models.CharField(max_length=255, null=True, blank=True), null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'grant'


class Publication(models.Model):
    """
    Represents Publication table in the DB
    """
    id = models.IntegerField(primary_key=True)
    doi = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField(Person, blank=True)
    grants = models.ManyToManyField(Grant, blank=True)
    issn = models.CharField(max_length=255, blank=True, null=True)
    keywords = ArrayField(base_field=models.CharField(max_length=255, null=True, blank=True), null=True, blank=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'publication'


class Dataset(models.Model):
    """
    Represents Dataset table in the DB
    """
    id = models.IntegerField(primary_key=True)
    doi = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField(null=True, blank=True)
    download_path = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    authors = models.ManyToManyField(Person, blank=True)
    grants = models.ManyToManyField(Grant, blank=True)
    publications = models.ManyToManyField(Publication, blank=True)

    class Meta:
        db_table = 'dataset'


class Asset(models.Model):
    """
    Represents Asset table in the DB
    """
    id = models.IntegerField(primary_key=True)
    doi = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    download_path = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    author_id = models.IntegerField(blank=True, null=True)
    grant_id = models.IntegerField(blank=True, null=True)
    publication_id = models.IntegerField(blank=True, null=True)
    dataset_id = models.IntegerField(blank=True, null=True)
    organization_id = models.IntegerField(blank=True, null=True)
    keywords = ArrayField(base_field=models.CharField(max_length=255, null=True, blank=True), null=True, blank=True)
    mime_type = models.CharField(max_length=255, blank=True, null=True)
    checksum = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'asset'
