from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder
from django import forms
# from dal import autocomplete
from posts.models import Post
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelectMultiple


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        labels = {
            "title": "Tytuł",
            "content": "Treść",
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            # self.helper.form_action = 'post:add'
            self.helper.form_action = 'tournaments: add_posts'
            self.helper.layout = Layout(
                Fieldset(
                    'Dodaj post',
                    'title',
                    'content',
                    'image'
                ),
                ButtonHolder(
                    Submit('submit', 'Dodaj', css_class='btn btn-primary'),
                    css_class="d-flex justify-content-end"
                )
            )
    def clean_post(self):
        data_value = self.cleaned_data.get("title")
        if  "huj" not in data_value:
            return data_value
        else:
            raise forms.ValidationError("trochę kultury może...")



class PostDeleteForm(forms.ModelForm):
    ButtonHolder(
        Submit('submit', 'Usuń', css_class='btn btn-primary'),
        css_class="d-flex justify-content-end"
    )

