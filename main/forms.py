from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder
from django import forms
from main.models import UserProfile


class ContactForm(forms.Form):
    email = forms.EmailField(label="Adres e-mail:")
    title = forms.CharField(label="Tytuł:")
    content = forms.CharField(widget=forms.Textarea, label="Treść wiadomości:")
    send_to_me = forms.BooleanField(required=False, label="Wyślij do mnie")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.from_action = 'contact'
        self.helper.layout = Layout(
            Fieldset(
                'Dane kontaktowe',
                'email',
            ),
            Fieldset(
                'Zawartość',
                'title',
                'content'
            ),
            Fieldset(
                'Dodtakowe',
                HTML("Zaznacz jeśli chcesz by wysłać kopię wiadomości do Ciebie"),
                'send_to_me'
            ),
            ButtonHolder(
                Submit('submit', 'Wyślij', css_class='btn btn-primary'),
                css_class="d-flex justify-content-end"
            )
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio"]

    labels = {
        "bio": "o sobie:",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'profile'
        self.helper.add_input(Submit('submit', 'Wyślij'))

