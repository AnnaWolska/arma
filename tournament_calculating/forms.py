from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from django import forms
from tournament_calculating.models import Group, ROUND_STATUS, ROUND_CONTUSIONS_STATUSES, ROUND_SPECIAL_STATUSES
from tournament_calculating.models import Participant, Fight, Round
from dal import autocomplete
from django.contrib.admin.widgets import AutocompleteSelectMultiple
from django.core.exceptions import ValidationError
from tournaments.models import Tournament


class CreateParticipantForm(forms.ModelForm):

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


class AddParticipantForm(forms.ModelForm):

    class Meta:
        # tournament = Tournament.objects.all()

        model = Group
        # tournament = Group.tournament
        # groups = Group.objects.filter(tournament=tournament)
        # print("tournament",tournament)
        # some_variable = ['participants']
        # avaible_participants = []
        #
        # for group in groups:
        #     print("group", group)
        #     participants.append(group.participants)
        #     print("participants", participants)
        # for p in some_variable:
        #     for participant in participants:
        #         if p != participant.name:
        #             avaible_participants.append(p)
        #
        # fields = avaible_participants

        fields = ['participants']
        labels = {"participants": 'uczestnicy'}
        widgets = {
            'participants': autocomplete.ModelSelect2Multiple(url='tournament_calculating:participant-autocomplete')
        }


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
        fields = ["points_fighter_one","points_fighter_two"]
        labels = {"points_fighter_one": 'punkty pierwszego zawodnika',
                  "points_fighter_two":'punkty drugiego zawodnika',
                  }

        # def clean(self):
        #     super(self).clean()
        #     points_fighter_one = self.cleaned_data.get(points_fighter_one)
        #     points_fighter_two = self.cleaned_data.get(points_fighter_two)
        #     if points_fighter_one in ['1','2','3','4','5'] and points_fighter_two in ['1','2','3','4','5']:
        #         self._errors['username'] = self.error_class([
        #             'Minimum 5 characters required'])

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.cleaned_data = None
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

    # def clean_points_fighter_one(self, *args, **kwargs):
    #
    #     points_fighter_one = self.cleaned_data.get("points_fighter_one")
        # if points_fighter_one == 2:
        #     raise ValidationError("sprawdzam czy wyskoczył błąd, że jest 2")
        # else:
        #     return points_fighter_one


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