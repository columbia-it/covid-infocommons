from ast import keyword
import imp
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings
from opensearchpy.client import OpenSearch
from rest_framework.views import APIView
from rest_framework.response import Response


class GrantSearch(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword', None)
        query = {
        }

        if not keyword:
            query['query'] = {'match_all': {}}
        else:
            query['query'] = {
                'multi_match': {
                'query': keyword,
                'fields': ['title', 'abstract']
            }
        }
        
        client = OpenSearch(
            hosts = [{'host': settings.OPENSEARCH_URL, 'port': 443}],
            use_ssl = True,
            verify_certs = True,
        )

        count_response = client.count(body = query, index = 'grant_index')
        if count_response: 
            query['size'] = count_response.get('count')
        
        response = client.search(
            body = query,
            index = 'grant_index'
        )
        return JsonResponse(response)
