from django.urls import path
from . import views

urlpatterns = [
    path("lessons/", views.placeholder),
]