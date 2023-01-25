from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from django import forms
from tournament_calculating.models import Group
from tournament_calculating.models import Participant, Fight, Round
from dal import autocomplete
from django.contrib.admin.widgets import AutocompleteSelectMultiple


# class ParticipantForm(forms.ModelForm):
#     class Meta:
#         model = Participant
#         fields = ['name', 'school', 'image']
#         labels = {
#             "name": "Imię i nazwisko",
#             "school": "Szkoła",
#             "image": "zdjęcie",
#         }
#
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.helper = FormHelper()
#             self.helper.form_method = 'post'
#             self.helper.form_action = 'tournament_calculating: add_participant'
#             self.helper.layout = Layout(
#                 Fieldset(
#                     'Dodaj uczestnika',
#                     'Imię i nazwisko',
#                     'szkoła',
#                     'zdjęcie'
#                 ),
#                 ButtonHolder(
#                     Submit('submit', 'Dodaj', css_class='btn btn-primary'),
#                     css_class="d-flex justify-content-end"
#                 )
#             )
class CreateParticipantForm(forms.ModelForm):
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
            self.helper.form_action = 'tournament_calculating: create_participant'
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

# ParticipantFormSet = forms.modelformset_factory(Participant, form=CreateParticipantForm)


class AddParticipantForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset=Participant.objects.all(),
        widget=autocomplete.Select)

    class Meta:
    #     model = Participant
    #     fields = ["name"]
    #     labels = {
    #         "name": "uczestnik",
    #     }
    #     model = Group
    #     fields =["participants"]
    #     labels = {
    #         "participants": "uczestnicy",


        model = Group
        fields =["name"]
        labels = {
            "name": "uczestnicy",
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_action = 'tournament_calculating: add_participant'
            self.helper.layout = Layout(
                Fieldset(
                    'Dodaj uczestnika',
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



class AddPointsForm(forms.ModelForm):

    class Meta:
        model = Round

        fields = [
            # "resolved_fighter_one",
                  "points_fighter_one",
                  # "resolved_fighter_two",
                  "points_fighter_two"
                  ]

        labels = {"points_fighter_one": 'punkty pierwszego zawodnika',
                  "points_fighter_two":'punkty drugiego zawodnika',
                  # "resolved_fighter_one":"czy jest rozstrzygnięcie?",
                  # "resolved_fighter_two":"czy jest rozstrzygnięcie?"
                  }

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
        fields = ['color_fighter_one', 'color_fighter_two']
        labels = {"color_fighter_one": 'kolor opaski pierwszego zawodnika', "color_fighter_two": 'kolor opaski drugiego zawodnika'}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_action = 'tournament_calculating: add_group'
            self.helper.layout = Layout(
                Fieldset(
                    'Dodaj grupę',
                    # 'numer',
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


class GroupSummaryForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['number_outgoing']
        labels = {'number_outgoing': 'ilość wychodzących z grupy'}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_action = 'tournament_calculating: group_summary'
            self.helper.layout = Layout(
                Fieldset(
                    'wychodzący z grupy'
                ),
                ButtonHolder(
                    Submit('submit', 'Dodaj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )