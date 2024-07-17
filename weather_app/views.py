import requests
from django.shortcuts import render
from datetime import datetime, timedelta


def get_weather_data(city):
    api_key = "f6c3e9f0e3e96e784084f2d3dc21893f"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        city_weather = {
            "city": weather_data["name"],
            "temperature": weather_data["main"]["temp"],
            "description": weather_data["weather"][0]["description"],
            "icon": weather_data["weather"][0]["icon"],
        }
        return city_weather
    else:
        return None


def get_daily_forecast(city):
    api_key = "f6c3e9f0e3e96e784084f2d3dc21893f"
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

    response = requests.get(complete_url)
    forecast_data = response.json()

    if forecast_data["cod"] != "404":
        daily_forecasts = []
        today = datetime.now()
        for forecast in forecast_data["list"]:
            forecast_date = datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
            if today <= forecast_date < today + timedelta(days=4):
                daily_forecasts.append(
                    {
                        "day": forecast["dt_txt"],
                        "min_temp": forecast["main"]["temp_min"],
                        "max_temp": forecast["main"]["temp_max"],
                        "description": forecast["weather"][0]["description"],
                        "icon": forecast["weather"][0]["icon"],
                    }
                )
        return daily_forecasts
    else:
        return None


def compare_weather(request):
    weather_data = None
    daily_forecasts = None
    error_message = None

    if request.method == "POST":
        city = request.POST.get("city")
        if city:
            weather_data = get_weather_data(city)
            if weather_data:
                daily_forecasts = get_daily_forecast(city)
            else:
                error_message = "City not found. Please enter a valid city name."

    return render(
        request,
        "weather_app/index.html",
        {
            "weather_data": weather_data,
            "daily_forecasts": daily_forecasts,
            "error_message": error_message,
        },
    )
