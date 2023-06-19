from django.urls import path
from .utils import get_weather, get_news
from .views import weather_choice

urlpatterns = [
    path('weather', get_weather, name='weather'),
    path("news", get_news, name='news'),
    path('weather-choice', weather_choice, name='weather_choice')
]
