from django import forms
from .models import Weather


class WeatherForm(forms.Form):
    city = forms.CharField(max_length=30, required=False)
