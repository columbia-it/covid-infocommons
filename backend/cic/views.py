from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from apis.models import Grant, Person

def index(request):
    """Home view callable, for the home page."""
    return render(request, 'index.html', {'keywords': request.GET.get('keywords', '')})


def detail(request, grant_id):
    grant = get_object_or_404(Grant, pk=grant_id)
    return render(request, 'grant_detail.html', {'grant': grant})

def pi_detail(request, pi_id):
    person = get_object_or_404(Person, pk=pi_id)
    grants = Grant.objects.filter(principal_investigator__id=pi_id)
    return render(request, 'person_detail.html', {'person': person, 'grants': grants})