from . import views
from django.urls import path
urlpatterns = [
    path('',views.weather, name='weather'),
    path('api/weather/', views.weather_for_location, name='weather-api'),
]
