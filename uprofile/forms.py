from django import forms
import account.forms

from .models import UProfile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

try:
    from PIL import Image
except ImportError:
    import Image

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

class MemorySafeImageField(forms.ImageField):
    """Image field that checks the size and dimensions of the image in its
       metadata *before* trying to load the damn thing into memory.
       
       Pixel dimensions are important because images are loaded into memory
       as a bitmap, so MB can easily become GB when working with compressed
       image formats.
       
       Requires `max_dimensions` and `max_size` keyword arguments."""
    
    def __init__(self, *args, **kwargs):
        self.max_dimensions = kwargs.pop('max_dimensions')
        self.max_size = kwargs.pop('max_size')
        super(MemorySafeImageField, self).__init__(*args, **kwargs)
        
    def to_python(self, data):
        # this isn't a mistake - the ImageField.to_python method is what causes the problem
        f = super(forms.ImageField, self).to_python(data)
        if f is None:
            return None
        
        if f.size > self.max_size:
            raise ValidationError('Maximum filesize is %s. This file is %s' % (filesizeformat(self.max_size), filesizeformat(data.size)))

        try:
            dimensions = Image.open(f).size
        except IOError:
            raise forms.ValidationError(u'That doesn\'t appear to be an image')
        else:
            if dimensions[0] > self.max_dimensions[0] or dimensions[1] > self.max_dimensions[1]:
                raise forms.ValidationError(u'Maximum image dimensions are %sx%s px. This file is %sx%s px' % (self.max_dimensions + dimensions))
        
        f.seek(0)
        return super(MemorySafeImageField, self).to_python(data)


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
    kwargs = {'max_dimensions':(10000,10000), 'max_size': 1*1024*1024}
    image = MemorySafeImageField(**kwargs)
