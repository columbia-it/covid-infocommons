from django.shortcuts import render, HttpResponse

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
            # Save Person
            # Combine emails and other emails into emails
            emails = data.get('emails', None)
            other_emails = data.get('other_emails', None)
            if emails and other_emails:
                emails = emails + ',' + other_emails
            # Set orcid to None if NA
            orcid = data.get('orcid', None)
            websites = data.get('websites', None)
            if orcid and orcid == 'NA':
                orcid = None
            comments = data.get('person_comments', None)
            if comments:
                if data['additional_comments']:
                    comments = comments + ' , ' + data.get('additional_comments', None)
            person = Person(
                first_name = data.get('first_name', None),
                last_name = data.get('last_name', None),
                orcid = orcid,
                emails = emails,
                websites = websites,
                keywords = data.get('person_kw', None),
                desired_collaboration = data.get('desired_collaboration', None),
                comments = comments,
                approved = False
            )
            person.save()

            # Save Grant
            award_id = data.get('award_id', None)
            award_title = data.get('award_title', None)
            funder = data.get('funder', None)
            grant_keywords = data.get('grant_kw', None)
            grant_additional_keywords = data.get('grant_add_kw', None)
            if grant_additional_keywords:
                keywords = grant_keywords + grant_additional_keywords
            funder_obj = None
            if funder:
                try:
                    funder_obj = Funder.objects.get(name=funder)
                except:
                    funder_obj = Funder(name=funder, approved=False)
                    funder_obj.save()

            grant = Grant(
                award_id = award_id,
                title = award_title,
                funder = funder_obj,
                keywords = keywords,
                approved = False,
                principal_investigator = person
            )
            grant.save()
            # Save publication
            dois = data.get('dois', None)
            if dois:
                if ',' in dois:
                    doi_list = dois.split(',')
                    for doi in doi_list:
                        p = Publication(doi=doi, grants=[grant])
                        p.save()
                else:
                    p = Publication(doi=dois)
                    p.save()
                    p.grants.add(grant)
                    p.save()

        except Exception as e:
            print(e)
    return HttpResponse('')