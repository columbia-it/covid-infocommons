from django.shortcuts import render
from .forms import PISurveyform


def index(request):
    return render(request, 'survey_form.html', {})
