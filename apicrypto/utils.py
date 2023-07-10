import json
import requests
import os
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from django.shortcuts import render
from apicrypto.models import Weather
from .forms import WeatherForm

load_dotenv()


@login_required
def get_weather(request, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv("api_key_weather")}'
    response = requests.get(url)
    weather_data = response.json()
    weather_data_main = weather_data['main']
    weather_dict = {
        "city": city,
        "temperature": weather_data_main['temp'],
        "feels_like": weather_data_main['feels_like'],
        'humidity': weather_data_main['humidity']
    }
    load_to_db_weather(weather_dict)
    return render(request, 'weather.html', {'weather_dict': weather_dict})


def load_to_db_weather(obj):
    try:
        data = Weather.objects.get(city=obj['city'])
        data.temperature = obj['temperature']
        data.feels_like = obj['feels_like']
        data.humidity = obj['humidity']
        data.save()
    except Weather.DoesNotExist:
        save_city_data = Weather.objects.create(**obj)
        save_city_data.save()


@login_required
def get_news(request, country='ru'):
    url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={os.getenv("api_key_news")}'
    response = requests.get(url)
    news_data = response.json()
    with open('news.txt', 'w') as news:
        json.dump(news_data, news)
    return render(request, 'news.html', {'news_data': news_data})
