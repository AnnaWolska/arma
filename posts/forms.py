from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder
from django import forms
# from dal import autocomplete
from posts.models import Post
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelectMultiple


class PostForm(forms.ModelForm):
    # tags = forms.ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=autocomplete.ModelSelect2Multiple(url='tags:tag-autocomplete'
    #     ))
    # categories = forms.ModelMultipleChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=autocomplete.ModelSelect2Multiple(url='posts:category-autocomplete'
    #     ))

    class Meta:
        model = Post
        fields = ['title', 'content', 'tournament', 'image']
        labels = {
            "title": "Tytuł",
            "content": "Treść",
            "tournament": "turniej"
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


class PostDeleteForm(forms.ModelForm):
    ButtonHolder(
        Submit('submit', 'Usuń', css_class='btn btn-primary'),
        css_class="d-flex justify-content-end"
    )

