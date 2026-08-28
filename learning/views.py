from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, Completion, QuizAttempt


def home(request):
    lessons = Lesson.objects.all().order_by("order")
    return render(request, "learning/home.html", {"lessons": lessons})


@login_required
def progress(request):
    completed_lesson_ids = set(
        Completion.objects.filter(user=request.user).values_list("lesson_id", flat=True)
    )

    lessons = Lesson.objects.all().order_by("order")
    total_lessons = lessons.count()
    lessons_done = len(completed_lesson_ids)

    lesson_rows = [
        {
            "lesson": lesson,
            "read": lesson.id in completed_lesson_ids,
        }
        for lesson in lessons
    ]

    percent = float((lessons_done / total_lessons) * 100) if total_lessons else 0

    return render(request, "learning/progress.html", {
        "lesson_rows": lesson_rows,
        "percent": percent,
        "lessons_done": lessons_done,
        "total_lessons": total_lessons,
    })

