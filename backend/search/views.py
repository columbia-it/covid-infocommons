from django.http import JsonResponse
from django.conf import settings
from opensearchpy.client import OpenSearch
from dateutil import parser
from datetime import datetime
import logging

logger = logging.getLogger('search.view')

def get_facet_by_field(request) :
    field_name = request.GET.get('field', None)
    client = OpenSearch(
        hosts = [{'host': settings.OPENSEARCH_URL, 'port': 443}],
        use_ssl = True,
        verify_certs = True,
    )

    query = {
        "size": 0,
        "aggs" : {
            "patterns" : {
                "terms" : { 
                    "field" : "{}.keyword".format(field_name),
                    "size": 10000,
                    "order": { "_key" : "asc" }
                }
            }
        }
    }

    response = client.search(
        body = query,
        index = 'grant_index',
    )

    return JsonResponse(response)


# Handle the request to search grants with keyword and/or filter values
def search_grants(request):
    logger.info('View--Grants search started at: {}'.format(datetime.now()))
    start = request.GET.get('from', 0)
    size = request.GET.get('size', 20)

    # Get filter/search criteria from request
    keyword = request.GET.get('keyword', None)
    funder_division = request.GET.get('funder_division', None)
    nsf_division = request.GET.get('nsf_division', None)
    nih_division = request.GET.get('nih_division', None)

    awardee_organization = request.GET.get('awardee_organization', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    org_state = request.GET.get('org_state', None)
    pi_name = request.GET.get('pi_name', None)
    po_name = request.GET.get('po_name', None)
    funder_name = request.GET.get('funder_name', None)


    query = {
        'size': size,
        'from': start,
        'sort' : [
            '_score', 
            { 
                'start_date' : 'desc'
            },
        ],
        'query': {
            'bool': {
                'must': [],
                'filter': {
                    'term': {
                        'approved': True
                    }
                }
            }
        }
    }

    if keyword:
        keyword = keyword.strip()
        # Escape the keyword in case it contains any Elasticsearch reserved characters
        special_chars = ['-', ':', '/']
        for s in special_chars:
            if s in keyword:
                keyword = '\"{}\"'.format(keyword)
                break

        query['query']['bool']['must'].append({
            'query_string': {
                'query': '*{}*'.format(keyword),
                'default_operator': 'AND',
                'fields': [
                    'title',
                    'abstract',
                    'award_id',
                    'keywords',
                    'principal_investigator.full_name',
                    'other_investigators.full_name',
                    'awardee_organization.name'
                ]
            }
        })

    if awardee_organization:
        query['query']['bool']['must'].append(
            { 
                'match_phrase': { 
                    'awardee_organization.name': awardee_organization
                }
            },
        )

    if funder_division:  
        if 'match_phrase' in query:
               query['query']['bool']['must']['match_phrase'].append(
                   {
                       'funder_divisions': funder_division
                    }
               )
        else:
            query['query']['bool']['must'].append(
            {
                'match_phrase': {
                    'funder_divisions': funder_division
                }
            }
        )

    if nih_division:  
        if 'match_phrase' in query:
               query['query']['bool']['must']['match_phrase'].append(
                   {
                       'funder_divisions': nih_division
                    }
               )
        else:
            query['query']['bool']['must'].append(
            {
                'match_phrase': {
                    'funder_divisions': nih_division
                }
            }
        )

    if nsf_division:  
        if 'match_phrase' in query:
               query['query']['bool']['must']['match_phrase'].append(
                   {
                       'funder_divisions': nsf_division
                    }
               )
        else:
            query['query']['bool']['must'].append(
            {
                'match_phrase': {
                    'funder_divisions': nsf_division
                }
            }
        )

    if start_date:
        temp_start_date = parser.parse(start_date)
        if temp_start_date:
            start_date = temp_start_date.strftime('%Y-%m-%d')
            query['query']['bool']['must'].append(
                {"range": {"start_date": {"gte": start_date}}
            })
    
    if end_date:
        temp_end_date = parser.parse(end_date)
        if temp_end_date:
            end_date = temp_end_date.strftime('%Y-%m-%d') 
            query['query']['bool']['must'].append(
                {"range": {"end_date": {"lte": end_date}}
            })

    if org_state:
        query['query']['bool']['must'].append(
            {
                'match': {
                    'awardee_organization.state': org_state
                }
            }
        )

    if pi_name:  
        if 'match_phrase' in query:
               query['query']['bool']['must']['match_phrase'].append(
                   {
                       'principal_investigator.full_name': pi_name
                    }
               )
        else:
            query['query']['bool']['must'].append(
            {
                'match_phrase': {
                    'principal_investigator.full_name': pi_name
                }
            }
        )

    if po_name:  
        if 'match_phrase' in query:
               query['query']['bool']['must']['match_phrase'].append(
                   {
                       'program_officials.full_name': po_name
                    }
               )
        else:
            query['query']['bool']['must'].append(
            {
                'match_phrase': {
                    'program_officials.full_name': po_name
                }
            }
        )

    if funder_name:  
        if 'match_phrase' in query:
               query['query']['bool']['must']['match_phrase'].append(
                   {
                       'funder.name': funder_name
                    }
               )
        else:
            query['query']['bool']['must'].append(
            {
                'match_phrase': {
                    'funder.name': funder_name
                }
            }
        )
      
    client = OpenSearch(
        hosts = [{'host': settings.OPENSEARCH_URL, 'port': 443}],
        use_ssl = True,
        verify_certs = True,
    )

    response = client.search(
        body = query,
        index = 'grant_index'
    )
    logger.info('View--Grants search ended at: {}'.format(datetime.now()))
    return JsonResponse(response)

# Handle the request to search publications with keyword and/or filter values
def search_publications(request):
    start = request.GET.get('from', 0)
    size = request.GET.get('size', 20)
    
    keyword = request.GET.get('keyword', None)
    doi = request.GET.get('doi', None)
    author_name = request.GET.get('pi_name', None)

    query = {
        'size': size,
        'from': start,
        'sort' : [
            '_score', 
            { 
                'publication_date' : 'desc'
            },
        ],
        'query': {
            'bool': {
                'must': [],
                'filter': {
                    'term': {
                        'approved': True
                    }
                }
            }
        }
    }

    if keyword:
        query['query']['bool']['must'].append({
            'multi_match': {
                'query': keyword,
                'operator': 'and',
                'fields': [
                    'title', 
                    'doi',  
                    'authors.full_name',
                    'authors.first_name', 
                    'authors.last_name', 
                    'authors.orcid', 
                    'keywords', 
                    'authors.emails'
                ]
            }
        })
    
    if doi:
        query['query']['bool']['must'].append(
            {
                'match': {
                    'doi': doi
                }
            }
        )
    if author_name:  
        if 'match_phrase' in query:
               query['query']['bool']['must']['match_phrase'].append(
                   {
                       'authors.full_name': author_name
                    }
               )
        else:
            query['query']['bool']['must'].append(
            {
                'match_phrase': {
                    'authors.full_name': author_name
                }
            }
        )

    client = OpenSearch(
        hosts = [{'host': settings.OPENSEARCH_URL, 'port': 443}],
        use_ssl = True,
        verify_certs = True,
    )

    response = client.search(
        body = query,
        index = 'publication_index'
    )

    return JsonResponse(response)

def search_people(request):
    start = request.GET.get('from', 0)
    size = request.GET.get('size', 20)

    # Get filter/search criteria from request
    keyword = request.GET.get('keyword', None)
    affiliated_org_name = request.GET.get('org_name', None)

    query = {
        'size': size,
        'from': start,
        'query': {
            'bool': {
                'must': [],
                'filter': {
                    'term': {
                        'approved': True
                    }
                }
            }
        }
    }

    if keyword:
        query['query']['bool']['must'].append({
            'multi_match': {
                'query': keyword,
                'operator': 'and',
                'fields': [
                    'first_name', 
                    'last_name', 
                    'orcid', 
                    'keywords', 
                    'emails'
                ]
            }
        })

    if affiliated_org_name:
        query['query']['bool']['must'].append(
            { 
                'match_phrase': { 
                    'awardee_organization.name': affiliated_org_name
                }
            },
        )
      
    client = OpenSearch(
        hosts = [{'host': settings.OPENSEARCH_URL, 'port': 443}],
        use_ssl = True,
        verify_certs = True,
    )

    response = client.search(
        body = query,
        index = 'person_index'
    )

    return JsonResponse(response)

# Handle the request to search datasets with keyword and/or filter values
def search_datasets(request):
    start = request.GET.get('from', 0)
    size = request.GET.get('size', 20)

    # Get filter/search criteria from request
    keyword = request.GET.get('keyword', None)
    mime_type = request.GET.get('mime_type', None)

    query = {
        'size': size,
        'from': start,
        'query': {
            'bool': {
                'must': [],
                'filter': {
                    'term': {
                        'approved': True
                    }
                }
            }
        }
    }

    if keyword:
        query['query']['bool']['must'].append({
            'multi_match': {
                'query': keyword,
                'operator': 'and',
                'fields': [
                    'doi', 
                    'title', 
                    'mime_type', 
                    'keywords', 
                    'principal_investigator.full_name',
                    'other_investigators.full_name',
                    'awardee_organization.name'
                ]
            }
        })

    if mime_type:  
        query['query']['bool']['must'].append(
        {
            'match': {
                'mime_type': mime_type
            }
        })

    client = OpenSearch(
        hosts = [{'host': settings.OPENSEARCH_URL, 'port': 443}],
        use_ssl = True,
        verify_certs = True,
    )

    query = {
        'query': {
            'match_all': {}
        }
    }
    
    response = client.search(
        body = query,
        index = 'dataset_index'
    )

    return JsonResponse(response)

# Handle the request to search assets with keyword and/or filter values
def search_assets(request):
    client = OpenSearch(
        hosts = [{'host': settings.OPENSEARCH_URL, 'port': 443}],
        use_ssl = True,
        verify_certs = True,
    )
    query = {
        'query': {
            'match_all': {}
        }
    }

    response = client.search(
        body = query,
        index = 'asset_index'
    )

    return JsonResponse(response)
