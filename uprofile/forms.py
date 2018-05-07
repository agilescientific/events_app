from django import forms
import account.forms

from .models import UProfile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

class SettingsForm(account.forms.SettingsForm):

    field_order = ['firstname', 'lastname','email', 'about', 
                   'github', 'twitter', 'linkedin', 'birthdate', 'timezone']

    def __init__(self, *args, **kwargs):
        super(SettingsForm,self).__init__(*args, **kwargs)
        self.fields.pop('language')

    firstname = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)
    github = forms.CharField(max_length=50, required=False, label='Gihub Username')
    twitter = forms.CharField(max_length=50, required=False, label='Twitter Username')
    linkedin = forms.CharField(max_length=50, required=False, label='LinkedIn Username')
    about = forms.CharField(widget=forms.Textarea, max_length=100)
    birthdate = forms.DateField(widget=forms.SelectDateWidget(years=range(1910, 2015)))

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
