from django import forms
from .models import Weather


class WeatherForm(forms.Form):
    name_city = forms.CharField(max_length=30, required=False)
