from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder
from django import forms
from tournaments.models import Tournament, Organizer
from dal import autocomplete
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelectMultiple


class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = "__all__"


OrganizerFormSet = forms.modelformset_factory(Organizer, form=OrganizerForm)


class TournamentForm(forms.ModelForm):
    # tournaments = forms.ModelMultipleChoiceField(
    #     queryset=Tournament.objects.all(),
    #     widget=autocomplete.ModelSelect2Multiple(url='tournaments:tournament-autocomplete')
    # )
    # organizator = forms.ModelChoiceField(queryset=Organizer.objects.all(), required=False)

    class Meta:
        model = Tournament
        fields = ["title", "description", "organizer"]
        labels = {
            "title": "tytuł",
            "description": "opis",
            "organizer": "organizator"
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.from_method = 'post'
            self.helper.from_method = 'tournaments:add'
            # to jest dwa razy metod i działa, nie ma action, o co chodzi?
            self.helper.layout = Layout(
                Fieldset(
                    'title',
                    'description',
                    'organizer'
                    'image'
                ),
                ButtonHolder(
                    Submit('submit', 'Dodaj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )




