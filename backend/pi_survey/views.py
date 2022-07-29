from django.shortcuts import render, HttpResponse
from .forms import PISurveyform
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import json
from apis.models import Person

# def get_token(fnc):
#     def inner(*args, **kwargs):
#         fnc(*args, **kwargs)
#     return inner

def index(request):
    return render(request, 'survey_form.html', {})

@csrf_exempt
#@get_token
def submitForm(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person = Person(
            first_name = data.get('first_name', None),
            last_name = data.get('last_name', None),
            orcid = data.get('orcid', None),
            emails = data.get('emails')
        )
        person.save()
        return HttpResponse('')

