from django import forms
from . import models
from django.utils.translation import gettext_lazy as _


class ApplicationInstanceForm(forms.ModelForm):
    #Vacation
    # start_date = forms.DateField(label=_("Start Date"))
    # end_date = forms.DateField(label=_("End Date"))
    # payout_before = forms.BooleanField(label=_("Payout Before"))
    #Taxes
    # npd = forms.BooleanField(label=_("npd"))
    # start_date = forms.DateField(label=_("start_date"))


    class Meta:
        model = models.ApplicationInstance
        fields = ['content', 'date_created'] # ['content', 'start_date', 'end_date', 'payout_before', 'application']
        widgets = {
            'content': forms.HiddenInput(),
            'date_created': forms.HiddenInput(),
        }