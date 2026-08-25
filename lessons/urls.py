from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.lesson_list, name='list'),
    path('<int:pk>/', views.lesson_detail, name='detail'),
    path('<int:pk>/quiz/', views.lesson_quiz, name='quiz'),
]