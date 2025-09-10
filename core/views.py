from django.shortcuts import render
from weather.views import get_weather

def homePage(request):
    weather = get_weather(33.65097042297,35.856345605529)
    print(weather['weather'][0]['description'])
    return render(request,'core/home.html',{})