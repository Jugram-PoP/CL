# phishing_sim/urls.py

from django.urls import path
from . import views

app_name = "phishing_sim"

urlpatterns = [
    path("", views.scenario_list, name="scenario_list"),
    path("<int:pk>/", views.scenario_detail, name="scenario_detail"),
]