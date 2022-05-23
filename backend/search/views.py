from django.http import JsonResponse
from django.conf import settings
from opensearchpy.client import OpenSearch

def get_facet_by_field(request) :
    field_name = request.GET.get('field', None)
    print('get_facet_by_field()')
    print('field_name = ')
    print(field_name)
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
    keyword = request.GET.get('keyword', None)
    start = request.GET.get('from', 0)
    query = {
        'size': 1000,
        'from': start
    }
    
    if not keyword:
        query['query'] = {
            'match_all': {}
            }
    else:
        query['query'] = {
            'multi_match': {
                'query': keyword,
                'fields': ['title', 'abstract', 'award_id', 'keywords']
            }
        }
        
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