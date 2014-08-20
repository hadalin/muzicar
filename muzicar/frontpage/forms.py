from django.forms.models import ModelMultipleChoiceField
from profile.models import Instrument
from django.utils.translation import ugettext as _
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label=_(u"Username"),
                               max_length=80,
                               required=True,
                               )

    password = forms.CharField(label=_(u"Password"),
                               max_length=80,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': ''}),
                               )


class SearchForm(forms.Form):
    instruments = ModelMultipleChoiceField(queryset=Instrument.objects.all(), required=False)