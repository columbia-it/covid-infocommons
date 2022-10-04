from django.db import models
from django_mysql.models import ListCharField
import datetime

# Model to store the PI survey form data
class Survey(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    emails = models.TextField()
    other_emails = models.TextField(null=True, blank=True)
    orcid = models.CharField(max_length=1000)
    award_id = models.CharField(max_length=255)
    award_title = models.TextField()
    funder_name = models.CharField(max_length=255)
    grant_keywords = models.TextField(blank=True, null=True)
    grant_additional_keywords = models.TextField(blank=True, null=True)
    dois = models.TextField(blank=True, null=True)
    websites = models.TextField(blank=True, null=True)
    person_keywords = models.TextField(blank=True, null=True)
    desired_collaboration = models.TextField(null=True, blank=True)
    person_comments = models.TextField(null=True, blank=True)
    person_additional_comments = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    submission_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' - Added on: '+ str(self.submission_date)

    class Meta:
        db_table = 'survey'
        ordering = ['id']

