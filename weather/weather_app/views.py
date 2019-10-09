from django.shortcuts import render
import requests

def index(request):
    url = open('weather_app/api_call.txt','r').read()
    city = 'Cracow'
    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

    return render(request, 'weather_app/index.html') #returns the index.html template
