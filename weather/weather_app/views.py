from django.shortcuts import render, get_object_or_404, redirect
from .models import City, TravelPlan
from .forms import CityForm, PlanForm
import requests

def display_forecast(request):

    url = open('weather_app/api_keys.txt','r').read()
    cities = City.objects.all()

    if request.method == 'POST' and 'add_city' in request.POST:
        city_form = CityForm(data = request.POST)
        city_form.save()
    city_form = CityForm()

    if request.method == 'POST' and 'save_schedule' in request.POST:
        schedule_form = PlanForm(data = request.POST)
        if schedule_form.is_valid():
            schedule_form.save()
    schedule_form = PlanForm(data = request.POST)

    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city.name)).json()
        weather = {
            'city' : city.name,
            'temperature' : city_weather['main']['temp'],
            'pressure' : city_weather['main']['pressure'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            'id': city.id,
            }
        weather_data.append(weather)

    context = {'weather_data' : weather_data,
               'city_form' : city_form,
               'schedule_form': schedule_form,
               }

    # Current objects number:
    schedule_list = TravelPlan.objects.all()
    city_list = City.objects.all()
    for i in schedule_list:
        print(f'TravelPlan: {i.id}')
    for i in city_list:
        print(f'City: {i.id}')

    return render(request, 'index.html', context)

def delete_city(request, pk):

    city = get_object_or_404(City, pk=pk)

    if request.method == 'POST':
        city.delete()
        return redirect('/')

    return render(request, 'index.html', {'city': city})
