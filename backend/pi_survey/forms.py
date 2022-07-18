from dataclasses import fields
from django import forms
from django.forms import ModelForm

from apis.models import Person, Grant

class PISurveyform(ModelForm):
    pass

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name']

class GrantForm(ModelForm):
    class Meta:
        model = Grant
        fields = ['award_id']
