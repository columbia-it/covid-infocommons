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
        "size": 10,
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
    size = request.GET.get('size', 20)
    print('Start date on request = ')
    start_date = request.GET.get('startDate', None)
    print(start_date)

    print('End date on request = ')
    end_date = request.GET.get('endDate', None)
    print(end_date)

    query = {
        'size': size,
        'from': start
    }
    
    if not keyword:
        query['query'] = {
            'match_all': {}
            }
    else:
        # query['query'] = {
        #     'multi_match': {
        #         'query': keyword,
        #         'fields': ['title', 'abstract', 'award_id', 'keywords']
        #     }
        # }
        query['query'] = {
            'bool': {
                'must': [
                    {
                        'multi_match': {
                            'query': keyword,
                            'fields': ['title', 'abstract', 'award_id', 'keywords', 'funder_divisions']
                        }
                    }
                ]
            }
        }
        if start_date and end_date:
            query['query']['bool']['filter'] = [
                {
                    "range": {
                        "start_date": {
                            "gte": start_date,
                            "format": "yyyy-MM-ddThh:mm:ss"
                        }
                    }
                },
                {
                    "range": {
                        "end_date": {
                            "lte": end_date,
                            "format": "yyyy-MM-dd"
                        }
                    }
                }
            ]
        
    print(query)
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