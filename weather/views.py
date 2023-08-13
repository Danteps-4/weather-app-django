from django.shortcuts import render
import datetime
import requests

# Create your views here.
def index(request):
    API_KEY = open("API_KEY", "r").read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        city = request.POST["city"]

        weather_data, daily_forecasts = fetch_weather_forecast(city, API_KEY, current_weather_url, forecast_url)
        
        context = {
            "weather_data": weather_data,
            "daily_forecasts": daily_forecasts,
        }
        # print(context)
        return render(request, "weather/index.html", context)
    else:
        return render(request, "weather/index.html")
    
def fetch_weather_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response["coord"]["lat"], response["coord"]["lon"]
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        "city": city,
        "temperature": round(response["main"]["temp"] - 273.15, 2),
        "description": response["weather"][0]["description"],
        "icon": response["weather"][0]["icon"],
    }

    daily_forecasts = []
    for daily_data in forecast_response["daily"][:5]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A"),
            "min_temp": round(daily_data["temp"]["min"] - 273.15, 2),
            "max_temp": round(daily_data["temp"]["max"] - 273.15, 2),
            "description": daily_data["weather"][0]["description"],
            "icon": daily_data["weather"][0]["icon"],
        })

    return weather_data, daily_forecasts