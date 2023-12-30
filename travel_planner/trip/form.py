from django import forms
from django.forms import HiddenInput
from .models import Trip, Destination


class TripForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), empty_label=None)
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, user_id, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].initial = user_id

    class Meta:
        model = Trip
        exclude = ['user', 'destination']
