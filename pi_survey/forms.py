from django import forms


class PISurveyform(forms.Form):
    pi_email = forms.CharField(label='Email', max_length=100)