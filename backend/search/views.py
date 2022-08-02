from django.http import JsonResponse
from django.conf import settings
from opensearchpy.client import OpenSearch
from dateutil import parser

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
        index = 'grant_index'
    )

    return JsonResponse(response)


def search_grants(request):
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
        query['query']['bool']['must'].append({
            'multi_match': {
                'query': keyword,
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

    return JsonResponse(response)