from opensearchpy.client import OpenSearch
from django.conf import settings

def update_grant_in_index(grant):
    client = OpenSearch(
        hosts = [{'host': settings.OPENSEARCH_URL, 'port': 443}],
        use_ssl = True,
        verify_certs = True,
    )
    updated_grant = {
        'doc': {
            'principal_investigator': {
                'first_name': grant['pi']['first_name'],
                'last_name': grant['pi']['last_name'],
                'emails': grant['pi']['emails'],
                'private_emails':  grant['pi']['private_emails'],
                'full_name': grant['pi']['first_name'] + ' ' + grant['pi']['last_name']
            },
            'awardee_organization': {
                'id': grant['awardee_organization']['id'],
                'ror': grant['awardee_organization']['ror'],
                'name': grant['awardee_organization']['name'],
                'address': grant['awardee_organization']['address'],
                'city': grant['awardee_organization']['city'],
                'state': grant['awardee_organization']['state'],
                'zip': grant['awardee_organization']['zip'],
                'country': grant['awardee_organization']['country'],
                'approved': grant['awardee_organization']['approved']
            },
            'keywords': grant['keywords'],
            'id': grant['id'],
            'award_id': grant['award_id'],
            'title': grant['title'],
            'start_date': grant['start_date'],
            'end_date': grant['end_date'],
            'award_amount': grant['award_amount'],
            'abstract': grant['abstract'],
            'approved': grant['approved'],
            'program_reference_codes': grant['program_reference_codes'],
            'funder_divisions': grant['funder_divisions'],
            'funder': {
                'id': grant['funder']['id'],
                'ror': grant['funder']['ror'],
                'name': grant['funder']['name'],
                'approved': grant['funder']['approved']
            }
        }
    }
    update_resp = client.update(index='grant_index', id=grant.id, body=updated_grant)
    return update_resp

