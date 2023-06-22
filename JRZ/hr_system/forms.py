from django import forms
from . import models
from django.utils.translation import gettext_lazy as _

class DateInput(forms.DateInput):
    input_type = 'date'

class ApplicationInstanceForm(forms.ModelForm):
    class Meta:
        model = models.ApplicationInstance
        fields = ['content', 'date_created']

        widgets = {
            'content': forms.HiddenInput(), 
            'full_name': forms.HiddenInput(),     
        }


class ApplicationInstanceUpdateForm(forms.ModelForm):
    class Meta:
        model = models.ApplicationInstance
        fields = ['content', 'date_created', 'status']