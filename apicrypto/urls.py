from django.urls import path
from .utils import get_weather, get_news

urlpatterns = [
    path('weather', get_weather, name='weather'),
    path("news", get_news, name='news'),
]
