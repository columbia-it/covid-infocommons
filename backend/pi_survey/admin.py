from unicodedata import name
from django.contrib import admin
from .models import Survey
from apis.models import Person, Funder, Grant, Publication
from django.core.exceptions import ValidationError
from simple_history.admin import SimpleHistoryAdmin
from django.http import HttpResponse
import csv
import logging

logger = logging.getLogger(__name__)

# Customize the Django admin view to include surveys
class SurveyAdmin(SimpleHistoryAdmin):
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

    # Check if a person already exists with the given email. Return the person found.
    # If no person found, create one with the given attributes and return it.
    def get_person(self,obj):
        orcid = getattr(obj, 'orcid')
        try:
            if orcid != 'NA':
                person_result = Person.objects.filter(orcid__contains=orcid)
                if person_result and person_result.count() > 0:
                    return person_result[0]
            else:
                email = getattr(obj, 'email')
                person_result = Person.objects.filter(emails__contains=email)
                if person_result and person_result.len() > 0:
                    return person_result[0]
                person_result = Person.objects.filter(private_emails__contains=email)
                if person_result and person_result.count() > 0:
                    return person_result[0]    
        except:
            return None
        return None

    # Check if a grant exists with the given award ID. If one is found, return it.
    # If none is found, create a new grant with the given attributes and return it.
    def get_grant(self, obj):
        award_id = getattr(obj, 'award_id')
        funder = getattr(obj, 'funder_name')
        if funder and funder == 'NIH':
            funder = 'National Institutes of Health'
        elif funder and funder == 'NSF':
            funder = 'National Science Foundation'
        grants = Grant.objects.filter(
            award_id__contains=award_id, 
            funder__name=funder)
        if grants and grants.count() > 0:
            return grants[0]
        else:
            return None
        
    # Check if a funder exists with the given name. If one is found, return it.
    # If none is found, create a new funder with the given name and return it.
    def get_funder(self, name):
        try:
            funder = Funder.objects.get(name=name)
            return funder
        except:
            return None

    def get_publication(self, doi):
        try:
            publication = Publication.objects.get(doi=doi)
            return publication
        except Publication.DoesNotExist:
            return Publication(doi=doi)

    # Override save_model() in ModelAdmin so that we can persist the models and their relationships
    # when approved flag is set to true. 
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'approved'):
            try:
                person = self.get_person(obj)
                grant = self.get_grant(obj)
                is_copi = getattr(obj, 'is_copi')
                comments = getattr(obj, 'person_comments')
                comments += getattr(obj, 'person_additional_comments')
                desired_collaboration = getattr(obj, 'desired_collaboration')
                websites = getattr(obj, 'websites')
                if websites:
                    websites = websites.split(',')
                if person:
                    if not person.orcid:
                        setattr(person, 'orcid', getattr(obj, 'orcid'))
                    original_kws = person.keywords
                    new_kws = getattr(obj, 'person_keywords')
                    if new_kws:
                        new_kws = new_kws.split(',')
                    original_kws.extend(new_kws)
                    setattr(person, 'keywords', original_kws)
                    setattr(person, 'comments', comments)
                    setattr(person, 'desired_collaboration', desired_collaboration)
                    setattr(person, 'websites', websites)
                else:
                    kws = getattr(obj, 'person_keywords')
                    if kws:
                        kws = getattr(obj, 'person_keywords').split(',')
                    person = Person(
                        first_name = getattr(obj, 'first_name'),
                        last_name = getattr(obj, 'last_name'),
                        orcid = getattr(obj, 'orcid'),
                        emails = getattr(obj, 'email'),
                        websites = websites,
                        keywords = kws,
                        desired_collaboration = desired_collaboration,
                        comments = comments
                    )
                funder = self.get_funder(getattr(obj, 'funder_name'))
                if not funder:
                    funder = Funder(name=getattr(obj, 'funder_name'))
                if not grant:
                    grant_keywords = []
                    if getattr(obj, 'grant_keywords'):
                        grant_keywords = getattr(obj, 'grant_keywords').split(',')
                    if getattr(obj, 'grant_additional_keywords'):
                        grant_keywords.extend(
                            getattr(obj, 'grant_additional_keywords').split(','))
                    grant = Grant(
                        award_id = getattr(obj, 'award_id'),
                        title = getattr(obj, 'award_title'),
                        keywords = grant_keywords
                    )
                    grant.funder = funder 
                else:
                    grant_keywords = []
                    if grant.keywords:
                        grant_keywords = grant.keywords
                    if getattr(obj, 'grant_keywords'):
                        grant_keywords.extend(
                            getattr(obj, 'grant_keywords').split(',')
                        )
                    if getattr(obj, 'grant_additional_keywords'):
                        grant_keywords.extend(
                            getattr(obj, 'grant_additional_keywords').split(',')
                        )
                    if grant_keywords:
                        setattr(grant, 'keywords', grant_keywords)
                setattr(person, 'approved', True)
                setattr(funder, 'approved', True)
                setattr(grant, 'approved', True)
                person.save()
                funder.save()
                if (not grant.principal_investigator) and (not is_copi):
                    setattr(grant, 'principal_investigator', person)
                grant.save()
                if is_copi:
                    grant.other_investigators.add(person)
                    grant.save()
                dois = getattr(obj, 'dois')
                if dois:
                    if ',' in dois:
                        doi_list = dois.split(',')
                        for doi in doi_list:
                            p = self.get_publication(doi=doi)
                            setattr(p, 'approved', True)
                            p.save()
                            p.grants.add(grant)
                            p.save()
                    else:
                        p = self.get_publication(dois)
                        setattr(p, 'approved', True)
                        p.save()
                        p.grants.add(grant)
                        p.save()
                super().save_model(request, obj, form, change)
            except Exception as e:
                print(e)
                print('Error occurred while approving survey')
        else:
            super().save_model(request, obj, form, change)


admin.site.register(Survey, SurveyAdmin)