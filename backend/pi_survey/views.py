from ast import keyword
from unicodedata import name
from django.shortcuts import render, HttpResponse

from .forms import PISurveyform
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import json
from apis.models import Person, Grant, Funder, Publication

# def get_token(fnc):
#     def inner(*args, **kwargs):
#         fnc(*args, **kwargs)
#     return inner

def index(request):
    return render(request, 'survey_form.html', {})

@csrf_exempt
#@get_token
def submitForm(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Get Person related data and save Person
            # Combine emails and other emails into emails
            emails = data.get('emails', None)
            other_emails = data.get('other_emails', None)
            if emails and other_emails:
                emails = emails + ',' + other_emails
            # Set orcid to None if NA
            orcid = data.get('orcid', None)
            if orcid and orcid == 'NA':
                orcid = None
            person = Person(
                first_name = data.get('first_name', None),
                last_name = data.get('last_name', None),
                orcid = orcid,
                emails = emails,
            )
            # person.save()
            print('Saving person')
            print(person)

            # Get Grant related data and save Grant
            award_id = data.get('award_id', None)
            funder = data.get('funder', None)
            grant_keywords = data.get('grant_kw', None)
            grant_additional_keywords = data.get('grant_add_kw', None)
            print('Grant Keywords = ')
            print(grant_keywords)
            print('Grant Additional Keywords = ')
            print(grant_additional_keywords)
            if grant_additional_keywords:
                grant_keywords.join(',').join(grant_additional_keywords)
            if funder:
                funder_obj = Funder.objects.get(name=funder)
                print('found funder')
            print(funder_obj)
            grant = Grant(
                award_id = award_id,
                funder = funder_obj,
                keywords = grant_keywords,
                approved = False
            )
            print('Saving grant = ')
            print(grant_keywords)
            grant.save()
            dois = data.get('dois', None)
            print('dois')
            print(dois)
            if dois:
                if ',' in dois:
                    print('found commas in dois')
                    doi_list = dois.split(',')
                    for doi in doi_list:
                        p = Publication(doi=doi)
                        print('Saving Publication')
                        #p.save()
                else:
                    p = Publication(doi=dois)
                    #p.save()
                    print('Saving Publication')
                    print(p)

        except Exception as e:
            print(e)
    return HttpResponse('')


