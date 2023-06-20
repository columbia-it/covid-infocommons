from django.test import TestCase
from models import Survey

class SurveyTest(TestCase): 
    def setUp(self) -> None:
        test_data = Survey.objects.create(
           first_name = 'john',
           last_name = 'doe',
           orcid = '0000-1913-1284-0182',
           award_id = '1234567',
           award_title = 'testing survey',
           funder_name = '',
           personal_keywords = 'this, is, a, test',
        )
        return super().setUp()
    
    def test_fields_not_empty(self):
        survey = Survey(self.test_data)
        #Django function that checks the fields
        survey.full_clean()

        self.assertIsNotNone(survey.first_name)
        self.assertIsNotNone(survey.last_name)
        self.assertIsNotNone(survey.orcid)
        self.assertIsNotNone(survey.award_id)
        self.assertIsNotNone(survey.award_title)
        self.assertIsNotNone(survey.funder_name)