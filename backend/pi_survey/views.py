from django.shortcuts import render
from .forms import PISurveyform, PersonForm, GrantForm

def grant_create_view(request):
    # person_form = PersonForm()
    # grant_form = GrantForm()
    # context = {
    #     'person_form': person_form,
    #     'grant_form': grant_form
    # }
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if 'cancel_create' in request.POST:
            return render(request, 'new_survey_form.html', {})
        print(request.POST)
        # create a form instance and populate it with data from the request:
        #person_form = PersonForm(request.POST or None)
        #print(person_form.data['first_name'])
        # check whether it's valid:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # if person_form.is_valid():
        #     person_form.save()
        #     # process the data in form.cleaned_data as required
        #     return render(request, 'new_survey_form.html', {'person_form': person_form})
    # if a GET (or any other method) we'll create a blank form
    else:
        pass
    return render(request, 'new_survey_form.html', {})
