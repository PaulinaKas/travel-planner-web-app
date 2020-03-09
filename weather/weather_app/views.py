from django.shortcuts import render, get_object_or_404, redirect
from .models import City
from .forms import CityForm

import requests


def display_forecast(request):
    url = open('weather_app/api_keys.txt','r').read()
    cities = City.objects.all()

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'pressure' : city_weather['main']['pressure'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'index.html', context)

def delete_city(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        city.delete()
        return redirect('/')

    return render(request, 'index.html', {'city': city})
