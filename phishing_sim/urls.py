from django.urls import path
from . import views

app_name = 'phishing_sim'

urlpatterns = [
    path('', views.simulation, name='simulation'),
]