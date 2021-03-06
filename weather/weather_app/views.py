from django.shortcuts import redirect, render, get_object_or_404
from .models import City, List, Schedule
from .forms import CityForm, ScheduleForm
import requests

def home_page(request):
    return render(request, 'home.html', {'form': CityForm()})

def delete_city(request, city_id, list_id):

    city = get_object_or_404(City, pk=city_id)
    list_ = List.objects.get(id=list_id)

    if request.method == 'POST':
        city.delete()
        return redirect(list_)


def new_list(request):
    form = CityForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Schedule.objects.create()
        form.save(for_list = list_)
        return redirect(list_)

    return render(request, 'home.html', {"form": form})


def view_list(request, list_id):

    url = open('weather_app/api_keys.txt','r').read()
    list_ = List.objects.get(id=list_id)
    cities = list_.city_set.all()
    weather_data = []

    schedules_without_extraction = Schedule.objects.all().values()
    schedules = []
    '''
    schedule looks like:
    {'id': 1, 'text': "<QueryDict: {'csrfmiddlewaretoken': ['...'],
                                    'text': ['Lorem ipsum dolor sit a'],
                                    'save_schedule': ['']}>"}
    schedule.get('text') looks like:
    <QueryDict: {'csrfmiddlewaretoken': ['...'],
                 'text': ['Lorem ipsum dolor sit a'],
                 'save_schedule': ['']}>
    '''
    separ_str = "': ['" # string_appearing_behind_text
    index = 2 # index_of_element_of_list_where_wanted_text_occurs
    for schedule in schedules_without_extraction:
        if schedule.get('text') != '':
            extracted_text_field = schedule.get('text').split(separ_str)[index].split("'")[0]
            # below replace \n \r into breaklines
            extracted_text_field = extracted_text_field.replace('\\\\', '')
            extracted_text_field = extracted_text_field.replace('\\r', '')
            extracted_text_field = extracted_text_field.replace('\\n', '\n')
            schedules.append(extracted_text_field)
        else:
            schedules.append('')

    schedule_form = ScheduleForm()

    for idx, city in enumerate(cities):
        city_weather = requests.get(url.format(city.name)).json()
        weather = {
            'city' : city.name,
            'temperature' : city_weather['main']['temp'],
            'pressure' : city_weather['main']['pressure'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            'id': city.id,
            'schedule': schedules[city.id-1], # city.id-1 to avoid 'index out of range'
            }
        print(weather.values())
        weather_data.append(weather)


    form = CityForm()
    if request.method == 'POST':
        form = CityForm(data=request.POST)
        if form.is_valid():
            Schedule.objects.create()
            form.save(for_list=list_)
            return redirect(list_)


    return render(request, 'list.html', {'list': list_,
                                        'form': form,
                                        'schedule_form': schedule_form,
                                        'weather_data' : weather_data,
                                        })

def add_schedule(request, schedule_id, list_id):

    schedule = get_object_or_404(Schedule, pk=schedule_id)
    list_ = List.objects.get(id=list_id)

    if request.method == 'POST':
        schedule.text = request.POST
        schedule.save()
        return redirect(list_)
