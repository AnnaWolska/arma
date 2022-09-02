from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder
from django import forms
from tournament_calculating.models import Participant, Group, Fight, Round
from tournament_calculating.models import Group
from dal import autocomplete
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelectMultiple


# class TournamentCalculateForm(forms.ModelForm):
#     class Meta:
#         model =


class AddParticipantForm(forms.ModelForm):
    # groups = forms.ModelChoiceField(
    #     queryset=Group.objects.all(),
    #     widget=autocomplete.Select)

    class Meta:
        model = Participant
        fields = ['name', 'school', 'image']
        labels = {
            "name": "Imię i nazwisko",
            "school": "Szkoła",
            "image": "zdjęcie",
            # "groups": "grupa"
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            # self.helper.form_action = 'post:add'
            self.helper.form_action = 'tournament_calculating: add_participant'
            self.helper.layout = Layout(
                Fieldset(
                    'Dodaj uczestnika',
                    'Imię i nazwisko',
                    'szkoła',
                    'zdjęcie'
                ),
                ButtonHolder(
                    Submit('submit', 'Dodaj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )



# class AddGroupForm(forms.ModelForm):
#     pass


class SortGroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['participants']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            # self.helper.form_action = 'post:add'
            self.helper.form_action = 'tournament_calculating: group_sort'
            self.helper.layout = Layout(
                Fieldset(
                    'Sortowanie grup',
                ),
                ButtonHolder(
                    Submit('submit', 'Sortuj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )
#
# class DrawFightsForm(forms.ModelForm):
#
#     class Meta:
#         model =