from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder
from django import forms
from dal import autocomplete
from galleries.models import Gallery, Photo
from django.contrib import admin
# from django.contrib.admin.widgets import AutocompleteSelectMultiple


class GalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ["title","slug","description","status"]
        labels = {
            "title": "tytuł",
            "slug": "slug",
            "description": "opis",
            "status": "status"
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.from_action = 'galleries:add'
            self.helper.layout = Layout(
                Fieldset(
                    'Dodaj galerię',
                    'title',
                    'description',
                    'slug',
                    'status'
                ),
                ButtonHolder(
                    Submit('submit', 'Dodaj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["title","slug","short_description", "image", "source","status"]
        labels = {
            "title": "tytuł",
            "slug": "slug",
            "short_description": "opis",
            'image': "zdjęcie",
            'source': "źródło",
            'status':"status"
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.from_action = 'galleries:add_photo'
            # self.helper.from_method = 'galleries:add_photo'
            self.helper.layout = Layout(
                Fieldset(
                    'Dodaj zdjęcie',
                    'title',
                    'slug',
                    "short_description",
                    'image',
                    'source',
                    'status'
                ),
                ButtonHolder(
                    Submit('submit', 'Dodaj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )