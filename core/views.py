from django.shortcuts import render
from products.models import Product
from weather.views import get_weather
from openrouter_utils import get_ai_recommendation
from datetime import datetime
from django.core.cache import cache



def homePage(request):
    # Get current weather
    weather = get_weather(33.65097042297, 35.856345605529)
    Current_weather = weather.get('weather', [{}])[0].get('description', 'Unknown')
    Temperature = f"{weather.get('main', {}).get('temp', 'N/A')}°C"
    Humidity = f"{weather.get('main', {}).get('humidity', 'N/A')}%"
    Wind_speed = f"{weather.get('wind', {}).get('speed', 'N/A')} km/h"

    # Latest products
    latest_product = Product.objects.all()[:4]

    # Try to get AI suggestion (with cache)
    ai_cache_key = "ai_weather_suggestion"
    ai_suggestion = cache.get(ai_cache_key)

    if not ai_suggestion:
        try:
            ai_suggestion = get_ai_recommendation(
                prompt=(
                    f"Given the following weather data:\n"
                    f"- Condition: {Current_weather}\n"
                    f"- Temperature: {Temperature}\n"
                    f"- Humidity: {Humidity}\n"
                    f"- Wind Speed: {Wind_speed}\n"
                    f"- Date and Time: {datetime.now()}\n\n"
                    "Location: Lebanon / Beqaa region\n"
                    "Provide practical recommendations for farmers based on these conditions. "
                    "Format the response as clear key points without using any formatting symbols or markdown."
                ),
                system_message="You are a helpful recommendation engine. Provide concise, practical advice.",
                temperature=0.5
            )
            # Cache for 6 hours to reduce API calls
            cache.set(ai_cache_key, ai_suggestion, timeout=21600)
        except Exception as e:
            ai_suggestion = f"Could not get AI recommendations: {str(e)}"

    context = {
        'ai_weather_suggestion': ai_suggestion,
        'Current_weather': Current_weather,
        'temp': Temperature,
        'hum': Humidity,
        'wind': Wind_speed,
        'latest_product': latest_product,
    }

    return render(request, 'core/home.html', context)


# def homePage(request):
#     weather = get_weather(33.65097042297,35.856345605529)
#     Current_weather= f"{weather['weather'][0]['description']}"
#     Temperature= f"{weather['main']['temp']}°C"
#     Humidity= f"{weather['main']['humidity']}%"
#     Wind_speed= f"{weather['wind']['speed']} km/h"

#     latest_product = Product.objects.all()[0:4]


#     try:
#         ai_suggestion = get_ai_recommendation(
#             prompt = (
#                 f"Given the following weather data:\n"
#                 f"- Condition: {Current_weather}\n"
#                 f"- Temperature: {Temperature}\n"
#                 f"- Humidity: {Humidity}\n"
#                 f"- Wind Speed: {Wind_speed}\n"
#                 f"- Date and Time: {datetime.now()}\n\n"
#                 "location: lebanon / beqaa region"
#                 "Provide practical recommendations for farmers based on these conditions. "
#                 "Format the response as clear key points without using any formatting symbols like ** or markdown styles."
#             ),

#             system_message="You are a helpful recommendation engine. Provide concise, practical advice.",
#             temperature=0.5
#         )
#         context = {
#             'ai_weather_suggestion': ai_suggestion,
#             'Current_weather':Current_weather,
#                'temp':Temperature,
#                'hum':Humidity,
#                'wind':Wind_speed,
#                'latest_product':latest_product
#         }
#         return render(request,'core/home.html',context)
#     except Exception as e:
#         context = {
#             'ai_weather_suggestion': f"Could not get AI recommendations: {str(e)}",
#             'Current_weather':Current_weather,
#                'temp':Temperature,
#                'hum':Humidity,
#                'wind':Wind_speed,
#                'latest_product':latest_product
#         }
#         return render(request, 'core/home.html', context)
    
    
    




        
        


