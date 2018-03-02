# -*- coding: utf-8 -*-
from django import forms
from .models import Team

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from ajax_select.fields import AutoCompleteSelectMultipleField


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
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