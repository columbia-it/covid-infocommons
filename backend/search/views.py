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
                "terms" : { "field" : "{}.keyword".format(field_name) }
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
    nsf_directorate = request.GET.get('nsf_directorate', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    query = {
        'size': size,
        'from': start,
        'query': {
            'bool': {
                'must': []
            }
        }
    }

    if keyword:
        query['query']['bool']['must'].append({
            'multi_match': {
                'query': keyword,
                'fields': ['title', 'abstract', 'award_id', 'keywords']
            }
        })

    if nsf_directorate:     
        query['query']['bool']['must'].append(
            {
                'match_phrase': {
                    'funder_divisions': nsf_directorate
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