from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class WeatherAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("compare_weather")

    @patch("weather_app.views.get_weather_data")
    @patch("weather_app.views.get_daily_forecast")
    def test_valid_city(self, mock_get_daily_forecast, mock_get_weather_data):
        # Mock the responses for a valid city
        mock_get_weather_data.return_value = {
            "city": "London",
            "temperature": 15,
            "description": "clear sky",
            "icon": "01d",
        }
        mock_get_daily_forecast.return_value = [
            {
                "day": "2024-07-17 12:00:00",
                "min_temp": 10,
                "max_temp": 20,
                "description": "clear sky",
                "icon": "01d",
            },
            {
                "day": "2024-07-18 12:00:00",
                "min_temp": 12,
                "max_temp": 22,
                "description": "light rain",
                "icon": "10d",
            },
            {
                "day": "2024-07-19 12:00:00",
                "min_temp": 14,
                "max_temp": 24,
                "description": "scattered clouds",
                "icon": "03d",
            },
        ]

        response = self.client.post(self.url, {"city": "London"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "London")

        self.assertTemplateUsed(response, "weather_app/index.html")

    @patch("weather_app.views.get_weather_data")
    def test_invalid_city(self, mock_get_weather_data):
        mock_get_weather_data.return_value = None

        response = self.client.post(self.url, {"city": "InvalidCity"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "City not found. Please enter a valid city name.")
        self.assertTemplateUsed(response, "weather_app/index.html")

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "weather_app/index.html")
