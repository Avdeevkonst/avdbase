from django.shortcuts import render

from avddisk.utils import title, possibility
from .forms import WeatherForm
from .utils import get_weather


def weather_choice(request):
    form = WeatherForm()
    if request.method == 'POST':
        input_value = request.POST.get('city')
        if form.is_valid():
            get_weather(input_value)
        else:
            form = WeatherForm()
    context = {
        'title': title,
        'possibility': possibility,
        'form': form
    }
    return render(request, 'weather_choice.html', context=context)
