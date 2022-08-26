from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder
from django import forms
from tournament_calculating.models import Participant, Group, Fight, Round
# from dal import autocomplete
from django.contrib import admin
# from django.contrib.admin.widgets import AutocompleteSelectMultiple


# class tournament_calculate_form(forms.ModelForm):
#     class Meta:
#         model =