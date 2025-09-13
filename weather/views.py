import requests
import json
from django.shortcuts import render
from django.core.cache import cache
from groq import Groq
import os
from datetime import datetime
from django.conf import settings

OPENWEATHER_API_KEY = settings.OPENWEATHER_API_KEY
GROQ_API_KEY = settings.GROQ_API_KEY

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"OpenWeather API Error: {e}")
        return None

def get_weather_forcast(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&appid=${OPENWEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"OpenWeather forcast API Error: {e}")
        return None


def generate_ai_advice(weather, forcast):
    cache_key = f"ai_advice:{json.dumps(weather, sort_keys=True)}"
    
    cached_advice = cache.get(cache_key)
    if cached_advice:
        print("✅ Serving advice from cache")
        print(datetime.now())
        return cached_advice
    
    # Process the 5-day forecast data to create a summary
    forecast_summary = []
    if forcast and 'list' in forcast:
        daily_forecasts = {}
        for item in forcast['list']:
            date = datetime.fromtimestamp(item['dt']).date()
            if date not in daily_forecasts:
                daily_forecasts[date] = {
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'weather_desc': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed'],
                    'pop': item['pop'] # Probability of precipitation
                }
            else:
                # Update min/max temps and average other values
                daily_forecasts[date]['temp_min'] = min(daily_forecasts[date]['temp_min'], item['main']['temp_min'])
                daily_forecasts[date]['temp_max'] = max(daily_forecasts[date]['temp_max'], item['main']['temp_max'])
                # For simplicity, we'll just take the last reported wind and weather for the day
                daily_forecasts[date]['weather_desc'] = item['weather'][0]['description']
                daily_forecasts[date]['wind_speed'] = max(daily_forecasts[date]['wind_speed'], item['wind']['speed'])
                daily_forecasts[date]['pop'] = max(daily_forecasts[date]['pop'], item['pop'])

        for date, data in sorted(daily_forecasts.items()):
            day_name = date.strftime('%A')
            summary_line = (
                f"{day_name} ({date.strftime('%Y-%m-%d')}): "
                f"Conditions: {data['weather_desc']}, "
                f"Temp: {data['temp_min']}°C to {data['temp_max']}°C, "
                f"Wind: {data['wind_speed']} km/h, "
                f"Rain Probability: {int(data['pop'] * 100)}%"
            )
            forecast_summary.append(summary_line)
    
    forecast_text = "\n".join(forecast_summary) if forecast_summary else "No forecast data available."

    prompt = f"""
    Current weather: {weather['weather'][0]['description']}
    Temperature: {weather['main']['temp']}°C
    Humidity: {weather['main']['humidity']}%
    Wind speed: {weather['wind']['speed']} km/h
    Date: {datetime.now()}
    
    5-Day Weather Forecast:
    {forecast_text}

    You are an agricultural expert.
    Based on the current weather and the 5-day forecast, provide professional farming advisory in strict JSON format only.
    Pay close attention to upcoming changes in temperature, wind, and precipitation from the forecast data to generate relevant weather alerts.
    pls always give me weather alerts dont keep it none pls.
    Use this structure exactly (no extra text, no explanation):

    {{
      "watering": "...",
      "fertilization": "...",
      "pest_risk": "...",
      "harvest": "...",
      "weather_alerts": [
        {{
          "title": "...",
          "description": "...",
          "time": "..."
        }}
      ]
    }}
    """
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
        )
        
        text = response.choices[0].message.content
        print("🔎 Groq raw output:", text)
        
        advice_dict = json.loads(text)
        cache.set(cache_key, advice_dict, 60 * 30)
        print("📦 Stored new advice in cache")
        
        return advice_dict

    except Exception as e:
        print("Groq Error:", e)
        return {
            "watering": "Check soil moisture regularly.",
            "fertilization": "Use balanced fertilizer as needed.",
            "pest_risk": "Monitor crops for pests daily.",
            "harvest": "Harvest crops based on ripeness.",
            "weather_alerts": [{"title": "API Error", "description": "Failed to generate AI advice.", "time": "N/A"}]
        }



def weather(request):
    lat = float(request.GET.get("lat", 33.8497))
    lon = float(request.GET.get("lon", 35.9042)) 

    current_weather = get_weather(lat, lon)
    forcast = get_weather_forcast(lat, lon)

    context = {
                "current_weather": current_weather,
                "weather_api" : settings.OPENWEATHER_API_KEY,
        }
    
    if request.method == "POST":
        ai_advisory = generate_ai_advice(current_weather,forcast) if current_weather else None
        print(ai_advisory)
        context = {
                "current_weather": current_weather,
                "ai_advisory": ai_advisory,
                "weather_api" : settings.OPENWEATHER_API_KEY,
        }
        return render(request, "weather/weather.html", context)
    
    return render(request, "weather/weather.html", context)


# def weather(request):
#     lat = float(request.GET.get("lat", 33.8497))
#     lon = float(request.GET.get("lon", 35.9042)) 

#     current_weather = get_weather(lat, lon)
#     forcast = get_weather_forcast(lat, lon)

    
#     ai_advisory = generate_ai_advice(current_weather,forcast) if current_weather else None
#     print(ai_advisory)
#     context = {
#         "current_weather": current_weather,
#         "ai_advisory": ai_advisory,
#         "weather_api" : settings.OPENWEATHER_API_KEY,
#     }
   
#     return render(request, "weather/weather.html", context)


def weather_for_location(request):
    return render(request, 'weather/weather_farm.html', {})

