from django import forms
from . import models


class ApplicationInstanceForm(forms.ModelForm):
    
    class Meta:
        model = models.ApplicationInstance
        fields = ("application", "date_created", "status", "content")