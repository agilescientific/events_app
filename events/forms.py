# -*- coding: utf-8 -*-
from django import forms
from .models import Organization, Project

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from ajax_select.fields import AutoCompleteSelectMultipleField

from markdownx.fields import MarkdownxFormField

from django.urls import reverse

from taggit.forms import TagField

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'members']

    name = forms.CharField()
    members = AutoCompleteSelectMultipleField('users')

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
                            Field('name', css_class='input-xlarge'),
                            'members',
                            FormActions(
                                Submit('save_changes', 'Create', css_class="btn-primary"),
                                Button('cancel', 'Cancel', onclick='history.go(-1);'),
                            )
                          )

class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['detail_long'].label = "Long Description (Markdown)"
        self.fields['detail_small'].label = "Short Description"
        # self.fields['resources'].label = "URLs of relevant info (separated by commas)"

    class Meta:
        model = Project
        fields = ['name', 'members', 'detail_small', 'detail_long', 'resources', 'github']
        # labels = ['Name', 'Members', 'Short Description', 'Long Description (Markdown)', 'resources', 'URL to Github Repo']

        widgets = {
          'detail_small': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

    name = forms.CharField(label='Project Name')
    github = forms.URLField(label='URL to Github Repo')
    detail_small = forms.Textarea()
    detail_long = MarkdownxFormField()
    members = AutoCompleteSelectMultipleField('users')
    resources = TagField()

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
                            Field('name', css_class='input-xlarge'),
                            'members',
                            Field('detail_small'),
                            Field('detail_long', style='width:100%;'),
                            # HTML('<small id="emailHelp" class="form-text text-muted">Input the URLs separated by commas</small>'),
                            'resources',
                            'github',
                            FormActions(
                                Submit('save_changes', 'Save', css_class="btn-primary"),
                                HTML("<a class='btn' href='{% url 'event-projects' slug=event.slug %}' role='button'>Cancel</a>")
                            )
                          )

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()