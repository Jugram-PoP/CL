from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Lesson


@login_required
def lessons(request):
    lessons = Lesson.objects.all()
    return render(request, 'lessons/lessons.html', {'lessons': lessons})


@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'lessons/lesson_detail.html', {'lesson': lesson})