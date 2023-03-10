from opensearchpy.client import OpenSearch
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def update_grant_in_grant_index(grant):
    client = OpenSearch(
        hosts = [{'host': settings.OPENSEARCH_URL, 'port': 443}],
        use_ssl = True,
        verify_certs = True,
    )
    query_body = {
        "query": {
            "ids" : {
                "values" : [12720]
            }
        }
    }
    try:
        # Query search index
        response = client.search(index="grant_index", body=query_body)
        if response['hits']['total']['value'] == 1:
            document = response['hits']['hits'][0]
            updated_grant = {
                'doc': {
                    'keywords': grant.keywords,
                    'funder_divisions': grant.funder_divisions,
                    'program_reference_codes': grant.program_reference_codes,
                    'award_id': grant.award_id,
                    'title': grant.title,
                    'start_date': grant.start_date,
                    'end_date': grant.end_date,
                    'award_amount': grant.award_amount,
                    'abstract': grant.abstract,
                    'approved': grant.approved
                }
            }
            update_resp = client.update(index='grant_index', id=document['_id'], body=updated_grant)
            logger.info(update_resp)
    except Exception as e:
        logger.error('Error occured while updating a grant in index') 
        logger.debug(e) 

# Update grants in the search index where PI is the given person 
def update_person_in_grant_index(person):
    client = OpenSearch(
        hosts = [{'host': settings.OPENSEARCH_URL, 'port': 443}],
        use_ssl = True,
        verify_certs = True,
    )

    query_body = {
        "query": {
            "match": {
                "principal_investigator.id": person.id
            }
        }
    }

    try:
        # Query search index
        response = client.search(index="grant_index", body=query_body)
        # Update PI data in each grant that has this person as PI 
        for grant in response['hits']['hits']:
            updated_grant = {
                'doc': {
                    'principal_investigator': {
                        'first_name': person.first_name,
                        'last_name': person.last_name,
                        'emails': person.emails,
                        'private_emails':  person.private_emails,
                        'full_name': person.first_name + ' ' + person.last_name
                    }
                }
            }
            update_resp = client.update(index='grant_index', id=grant['_id'], body=updated_grant)
            logger.info(update_resp)
    except Exception as e:
        logger.error('Error occured while updating PI of a grant in index') 
        logger.debug(e)

