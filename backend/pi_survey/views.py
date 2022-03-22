from django.shortcuts import render
from .forms import PISurveyform


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PISurveyform(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            return render(request, 'survey_form.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PISurveyform()

    return render(request, 'survey_form.html', {'form': form})
