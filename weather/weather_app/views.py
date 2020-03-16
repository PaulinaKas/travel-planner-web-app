from django.shortcuts import redirect, render, get_object_or_404
from .models import City, List
from .forms import CityForm
import requests

def home_page(request):
    return render(request, 'home.html', {'form': CityForm()})

def delete_city(request, city_id, list_id):

    city = get_object_or_404(City, pk=city_id)
    list_ = List.objects.get(id=list_id)

    if request.method == 'POST':
        city.delete()
        return redirect(list_)

    return render(request, 'home.html', {'city': city})


def new_list(request):
    form = CityForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


def view_list(request, list_id):

    url = open('weather_app/api_keys.txt','r').read()
    list = List.objects.get(id=list_id)
    cities = list.city_set.all()
    weather_data = []

    # if request.method == 'POST' and 'save_schedule' in request.POST:
    #         schedule_form = PlanForm(data = request.POST)
    #         if schedule_form.is_valid():
    #             schedule_form.save()
    #     schedule_form = PlanForm()

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


    list_ = List.objects.get(id=list_id)
    form = CityForm()
    if request.method == 'POST':
        form = CityForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_,
                                        'form': form,
                                        'weather_data' : weather_data,
                                        })
