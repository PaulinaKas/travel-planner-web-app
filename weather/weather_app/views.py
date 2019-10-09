from django.shortcuts import render

def index(request):
    return render(request, 'weather_app/index.html') #returns the index.html template
