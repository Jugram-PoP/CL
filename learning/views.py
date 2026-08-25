from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, Completion, QuizAttempt


def home(request):
    lessons = Lesson.objects.all().order_by("order")
    return render(request, "learning/home.html", {"lessons": lessons})


@login_required
def progress(request):
    # 1. Get completed lesson IDs (Query 1)
    completed_lesson_ids = set(
        Completion.objects.filter(user=request.user).values_list("lesson_id", flat=True)
    )

    # 2. Get counts of correct user answers per lesson in a single query (Query 2)
    user_correct_counts = dict(
        QuizAttempt.objects.filter(user=request.user, is_correct=True)
        .values_list("question__lesson_id")
        .annotate(total=Count("id"))
        .values_list("question__lesson_id", "total")
    )

    # 3. Annotate lessons with total question counts (Query 3)
    lessons = Lesson.objects.annotate(total_questions=Count("questions"))
    total_lessons = lessons.count()

    lesson_rows = []
    quizzes_done = 0

    for lesson in lessons:
        correct_count = user_correct_counts.get(lesson.id, 0)
        # Quiz is complete if lesson has questions and user got them all right
        quiz_complete = lesson.total_questions > 0 and correct_count == lesson.total_questions

        if quiz_complete:
            quizzes_done += 1

        lesson_rows.append({
            "lesson": lesson,
            "read": lesson.id in completed_lesson_ids,
            "quiz_complete": quiz_complete,
        })

    lessons_done = len(completed_lesson_ids)
    total_points = total_lessons * 2
    earned_points = lessons_done + quizzes_done
    percent = float((earned_points / total_points) * 100) if total_points else 0

    return render(request, "learning/progress.html", {
        "lesson_rows": lesson_rows,
        "percent": percent,
        "lessons_done": lessons_done,
        "total_lessons": total_lessons,
        "quizzes_done": quizzes_done,
    })
