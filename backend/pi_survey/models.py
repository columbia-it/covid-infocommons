from dataclasses import fields
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

# Model to store the PI survey form data
class Survey(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=1000, verbose_name='First Name')
    last_name = models.CharField(max_length=1000, verbose_name='Last Name')
    email = models.CharField(max_length=1000)
    orcid = models.CharField(max_length=1000)
    award_id = models.CharField(max_length=255, verbose_name='Award ID')
    award_title = models.TextField(verbose_name='Award Title')
    funder_name = models.CharField(max_length=255, verbose_name='Funder Name')
    grant_keywords = models.TextField(blank=True, null=True)
    grant_additional_keywords = models.TextField(blank=True, null=True)
    dois = models.TextField(blank=True, null=True, verbose_name='DOIs')
    websites = models.TextField(blank=True, null=True)
    person_keywords = models.TextField(blank=True, null=True, verbose_name='Keywords')
    desired_collaboration = models.TextField(null=True, blank=True)
    person_comments = models.TextField(null=True, blank=True)
    person_additional_comments = models.TextField(null=True, blank=True, verbose_name='Communication preferences')
    approved = models.BooleanField(default=False)
    submission_date = models.DateTimeField(default=timezone.now)
    is_copi = models.BooleanField(default=False, verbose_name='Co-Pi tick box')
    history = HistoricalRecords()

    def __str__(self):
        approved_text = 'Approved' if self.approved else 'Not approved'
        return self.first_name + ' ' + self.last_name + ' - Added on: '+ str(self.submission_date) + ' - ' + approved_text

    class Meta:
        db_table = 'survey'
        ordering = ['id']