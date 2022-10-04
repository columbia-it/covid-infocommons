from django.contrib import admin
from .models import Survey
from apis.models import Person, Funder, Grant, Publication

# Customize the Django admin view to include surveys
class SurveyAdmin(admin.ModelAdmin):

    # Check if a person already exists with the given email. Return the person found.
    # If no person found, create one with the given attributes and return it.
    def get_person_object(self, obj):
        first_name = getattr(obj, 'first_name')
        last_name = getattr(obj, 'last_name')
        # Check if person already exists with the given first and last names
        person_result = Person.objects.filter(first_name=first_name, last_name=last_name).values()
        if person_result.count() > 0:
            person = Person.objects.get(id=person_result[0]['id'])
            return person
        else:
            # Combine emails and other emails into emails
            emails = getattr(obj, 'emails')
            other_emails = getattr(obj, 'other_emails')
            if emails and other_emails:
                emails = emails + ',' + other_emails
            # Set orcid to None if NA
            orcid = getattr(obj, 'orcid')
            websites = getattr(obj, 'websites')
            if orcid and orcid == 'NA':
                orcid = None
            comments = getattr(obj, 'person_comments')
            if comments:
                if getattr(obj, 'person_additional_comments'):
                    comments = comments + '. ' + getattr(obj, 'person_additional_comments')
            person = Person(
                first_name = first_name,
                last_name = last_name,
                orcid = orcid,
                emails = emails,
                websites = websites,
                keywords = getattr(obj, 'person_keywords'),
                desired_collaboration = getattr(obj, 'desired_collaboration'),
                comments = comments,
            )
            return person

    # Check if a grant exists with the given award ID. If one is found, return it.
    # If none is found, create a new grant with the given attributes and return it.
    def get_grant_object(self, obj):
        award_id = getattr(obj, 'award_id')
        try:
            grant = Grant.objects.get(award_id=award_id)
            return grant
        except Grant.DoesNotExist:
            award_title = getattr(obj, 'award_title')
            grant_keywords = getattr(obj, 'grant_keywords')
            grant_additional_keywords = getattr(obj, 'grant_additional_keywords')
            if grant_keywords and grant_additional_keywords:
                grant_keywords = grant_keywords + ',' + grant_additional_keywords
            elif not grant_keywords:
                grant_keywords = grant_additional_keywords
            grant = Grant(
                award_id = award_id,
                title = award_title,
                keywords = grant_keywords,
            )
            return grant
        
    # Check if a funder exists with the given name. If one is found, return it.
    # If none is found, create a new funder with the given name and return it.
    def get_funder_object(self, name):
        funder_obj = Funder.objects.get(name=name)
        if not funder_obj:
            funder_obj = Funder(name=name)
        return funder_obj

    def get_publication_object(self, doi):
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
                person = self.get_person_object(obj)
                setattr(person, 'approved', True)
                funder = self.get_funder_object(getattr(obj, 'funder_name'))
                setattr(funder, 'approved', True)
                grant = self.get_grant_object(obj)  
                grant.funder = funder 
                grant.principal_investigator = person
                setattr(grant, 'approved', True)
                person.save()
                funder.save()
                grant.save()
                dois = getattr(obj, 'dois')
                if dois:
                    if ',' in dois:
                        doi_list = dois.split(',')
                        for doi in doi_list:
                            p = self.get_publication_object(doi=doi)
                            setattr(p, 'approved', True)
                            p.save()
                            p.grants.add(grant)
                            p.save()
                    else:
                        p = self.get_publication_object(dois)
                        setattr(p, 'approved', True)
                        p.save()
                        p.grants.add(grant)
                        p.save()
            except Exception as e:
                print(e)
                print('Error occurred while saving survey')
        super().save_model(request, obj, form, change)

admin.site.register(Survey, SurveyAdmin)