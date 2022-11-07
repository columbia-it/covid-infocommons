from unicodedata import name
from django.contrib import admin
from .models import Survey
from apis.models import Person, Funder, Grant, Publication
from django.core.exceptions import ValidationError
from simple_history.admin import SimpleHistoryAdmin

# Customize the Django admin view to include surveys
class SurveyAdmin(SimpleHistoryAdmin):

    # Check if a person already exists with the given email. Return the person found.
    # If no person found, create one with the given attributes and return it.
    def get_person(self,obj):
        orcid = getattr(obj, 'orcid')
        try:
            if orcid != 'NA':
                person_result = Person.objects.get(orcid__contains=orcid)
                if person_result:
                    return person_result
            else:
                email = getattr(obj, 'email')
                person_result = Person.objects.get(emails__contains=email)
                if person_result:
                    return person_result
                person_result = Person.objects.get(private_emails__contains=email)
                if person_result:
                    return person_result        
        except:
            return None
        return None

    # Check if a grant exists with the given award ID. If one is found, return it.
    # If none is found, create a new grant with the given attributes and return it.
    def get_grant(self, obj):
        award_id = getattr(obj, 'award_id')
        funder = getattr(obj, 'funder_name')
        grants = Grant.objects.filter(
            award_id=award_id, 
            funder__name=funder)
        return grants
        
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
                grants = self.get_grant(obj)
                is_copi = getattr(obj, 'is_copi')
                comments = getattr(obj, 'person_comments')
                comments += getattr(obj, 'person_additional_comments')
                desired_collaboration = getattr(obj, 'desired_collaboration')
                websites = getattr(obj, 'websites')

                if person:
                    if not person.orcid:
                        setattr(person, 'orcid', getattr(obj, 'orcid'))
                    original_kws = person.keywords
                    new_kws = getattr(obj, 'person_keywords')
                    if original_kws:
                        original_kws = original_kws.append(new_kws)
                    else:
                        original_kws = new_kws
                    setattr(person, 'keywords', original_kws)
                    setattr(person, 'comments', comments)
                    setattr(person, 'desired_collaboration', desired_collaboration)
                    setattr(person, 'websites', websites)
                else:
                    person = Person(
                        first_name = getattr(obj, 'first_name'),
                        last_name = getattr(obj, 'last_name'),
                        orcid = getattr(obj, 'orcid'),
                        emails = getattr(obj, 'email'),
                        websites = websites,
                        keywords = getattr(obj, 'person_keywords'),
                        desired_collaboration = desired_collaboration,
                        comments = comments
                    )
                
                funder = self.get_funder(getattr(obj, 'funder_name'))
                if not funder:
                    funder = Funder(name=getattr(obj, 'funder_name'))
                if len(grants) == 0:
                    grant_keywords = []
                    if getattr(obj, 'grant_keywords'):
                        grant_keywords = getattr(obj, 'grant_keywords').split(',')
                    if getattr(obj, 'grant_additional_keywords'):
                        grant_keywords = grant_keywords.extend(
                            getattr(obj, 'grant_additional_keywords').split(','))
                    
                    grant = Grant(
                        award_id = getattr(obj, 'award_id'),
                        title = getattr(obj, 'award_title'),
                        keywords = grant_keywords
                    )
                    grant.funder = funder 
                else:
                    grant = grants[0]
                    grant_keywords = []
                    if grant.keywords:
                        grant_keywords = grant.keywords.split(',')
                    if getattr(obj, 'grant_keywords'):
                        grant_keywords = grant_keywords.extend(
                            getattr(obj, 'grant_keywords').split(',')
                        )
                    if getattr(obj, 'grant_additional_keywords'):
                        grant_keywords = grant_keywords.extend(
                            getattr(obj, 'grant_additional_keywords').split(',')
                        )
                    setattr(grant, 'keywords', grant_keywords)
                if (not grant.principal_investigator) and (not is_copi):
                    setattr(grant, 'principal_investigator', person)
                if is_copi:
                    #Grant.objects.filter(other_investigators__orcid=person.orcid)
                    grant.other_investigators.add(person)
                setattr(person, 'approved', True)
                setattr(funder, 'approved', True)
                setattr(grant, 'approved', True)
                person.save()
                funder.save()
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