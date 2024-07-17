from django.urls import path
from . import views

urlpatterns = [
    path('', views.compare_weather, name='compare_weather'),
]