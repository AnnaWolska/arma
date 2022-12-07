from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder
from django import forms
from tournament_calculating.models import Participant, Group, Fight, Round
from tournament_calculating.models import Group
from dal import autocomplete
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelectMultiple


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
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
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


class AddRoundsForm(forms.ModelForm):

    class Meta:
        model = Fight
        fields = ['rounds']
        labels = {"rounds": 'starcia'}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_action = 'tournament_calculating:tournament_calculate'
            self.helper.layout = Layout(
                Fieldset(
                    'Dodaj ilość starć',
                    'rounds',
                ),
                ButtonHolder(
                    Submit('submit', 'Dodaj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )

# class AddRoundsForm(forms.ModelForm):
#
#     class Meta:
#         model = Fight
#         fields = ['rounds']
#         labels = {"rounds": 'starcia'}
#
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.helper = FormHelper()
#             self.helper.form_method = 'post'
#             self.helper.form_action = 'tournament_calculating:tournament_calculate'
#             self.helper.layout = Layout(
#                 Fieldset(
#                     'Dodaj ilość starć',
#                     'rounds',
#                 ),
#                 ButtonHolder(
#                     Submit('submit', 'Dodaj', css_class='btn btn-primary'),
#                     css_class="d-flex justify-content-end"
#                 )
#             )





class AddPointsForm(forms.ModelForm):
    class Meta:
        pass
        model = Fight
        fields = ["fighter_one_points","fighter_two_points"]
        # fields = []
        labels = {"points": 'punkty'}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_action = 'tournament_calculating:add_points'
            self.helper.layout = Layout(
                Fieldset(
                        "punkty"
                ),
                ButtonHolder(
                    Submit('submit', 'Dodaj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )


class AddGroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['number']
        labels = {"number": 'numer'}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_action = 'tournament_calculating: add_group'
            self.helper.layout = Layout(
                Fieldset(
                    'Dodaj grupę',
                    'numer',
                ),
                ButtonHolder(
                    Submit('submit', 'Dodaj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )


class AddFightsForm(forms.ModelForm):

    class Meta:
        model = Fight
        fields = ['rounds']
        labels = {"rounds": 'rundy'}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_action = 'tournament_calculating: add_fights'
            self.helper.layout = Layout(
                Fieldset(
                    'Dodaj walki',
                    'rundy',
                ),
                ButtonHolder(
                    Submit('submit', 'Dodaj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )

