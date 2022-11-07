from django.shortcuts import render, HttpResponse, get_list_or_404

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import json

from urllib3 import HTTPResponse
from apis.models import Person, Grant, Funder, Publication
from .models import Survey
from django.http import Http404

# def get_token(fnc):
#     def inner(*args, **kwargs):
#         fnc(*args, **kwargs)
#     return inner

def index(request):
    return render(request, 'survey_form.html', {})

def send_email():
    from_address = ''
    to_address = ''
    
@csrf_exempt
#@get_token
def submitForm(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            survey = Survey(
                first_name = data.get('first_name', None),
                last_name = data.get('last_name', None),
                email = data.get('email', None),
                orcid = data.get('orcid', None),
                award_id = data.get('award_id', None),
                award_title = data.get('award_title', None),
                funder_name = data.get('funder', None),
                grant_keywords = data.get('grant_kw', None),
                grant_additional_keywords = data.get('grant_add_kw', None),
                dois = data.get('dois', None),
                websites = data.get('websites', None),
                person_keywords = data.get('person_kw', None),
                desired_collaboration = data.get('desired_collaboration', None),
                person_comments = data.get('person_comments', None),
                person_additional_comments = data.get('additional_comments', None),
                is_copi = data.get('is_copi', None)
            )
            survey.save()
        except Exception as e:
            print(e)
    return HttpResponse('')