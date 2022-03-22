from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


@require_http_methods(["GET"])
def search_grants(request):
    return JsonResponse({"test": "Hello"})
