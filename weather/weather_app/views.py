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
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'pressure' : city_weather['main']['pressure'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            }
        weather_data.append(weather)

    context = {'weather_data' : weather_data,
               'city_form' : city_form,
               'schedule_form': schedule_form,
               }

    return render(request, 'index.html', context)

def delete_city(request, pk):

    city = get_object_or_404(City, pk=pk)

    if request.method == 'POST':
        city.delete()
        return redirect('/')

    return render(request, 'index.html', {'city': city})

# def add_schedule(request, pk):
#
#     # city = get_object_or_404(City, pk=pk)
#     schedule_form = PlanForm()
#
#     if request.method == 'POST':
#         schedule_form = PlanForm(data = request.POST)
#         if schedule_form.is_valid():
#             schedule_form.save()
#             return redirect('/')
#
#     return render(request, 'index.html', {'schedule_form': schedule_form})

# if request.method == 'POST' and 'save_schedule' in request.POST:
#     schedule_form = PlanForm(data = request.POST)
#     if schedule_form.is_valid():
#         schedule_form.save()
# schedule_form = PlanForm(data = request.POST)
