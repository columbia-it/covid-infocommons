from django.http import JsonResponse
from django.conf import settings
from opensearchpy.client import OpenSearch

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
    keyword = request.GET.get('keyword', None)
    nsf_directorate = request.GET.get('nsf_directorate', None)

    query = {
        'size': size,
        'from': start
    }

    if not keyword and not nsf_directorate:
        query['query'] = {
            'match_all': {}
        }

    if keyword:
        query['query'] = {
            'bool': {
                'must': [
                    {
                        'multi_match': {
                            'query': keyword,
                            'fields': ['title', 'abstract', 'award_id', 'keywords']
                        }
                    }
                ]
            }
        }

    if nsf_directorate:
        if 'query' not in query:
            query['query'] = {'bool': {'must':[]}}
        elif 'bool' not in query['query']:
            query['query'].update({'bool': {'must':[]}})
        
        query['query']['bool']['must'].append(
            {
                'match_phrase': {
                    'funder_divisions': nsf_directorate
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