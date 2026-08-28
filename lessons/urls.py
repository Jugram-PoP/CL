from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.lesson_list, name='list'),
    path('<int:pk>/', views.lesson_detail, name='detail'),
    path("answer/", views.answer_question, name="answer_question"),
    path("<int:pk>/section/<int:section_index>/", views.lesson_section, name="section"),
]
