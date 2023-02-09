from rest_framework.test import APIRequestFactory, APITestCase
from factories import SurveyFactory
import random

class PISurveyViewTest(APITestCase):
    def setUp(self) -> None:
        self.survey = SurveyFactory()
        return super().setUp()

    def test_submit_form(self):
        url = f"/survey"
        request_data = {
            "data": {
                "type": "Survey",
                "attributes": {
                    "approved": True,
                    "first_name": self.survey.first_name, 
                    "last_name": self.survey.last_name,
                    "orcid": self.survey.orcid, 
                    "email": self.survey.email, 
                    "award_id": self.survey.award_id,
                    "additional_comments": self.survey.person_additional_comments,
                    "desired_collaboration": self.survey.desired_collaboration,
                    "dois": self.survey.dois,
                    "funder": self.survey.funder_name,
                    "grant_keywords": self.survey.grant_keywords,
                    "grant_add_kw": self.survey.grant_additional_keywords,
                    "is_copi": self.survey.is_copi,
                    "websites": self.survey.websites
                }
            }
        }
        response = self.client.post(url, data=request_data)
        print(response)
        assert response.status_code == 200, response.content.decode()


