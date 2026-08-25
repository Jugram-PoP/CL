from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lesson, Completion, Question, QuizAttempt


@login_required
def lesson_list(request):
    lessons = Lesson.objects.all()
    completed_ids = set(
        Completion.objects.filter(user=request.user).values_list("lesson_id", flat=True)
    )
    lessons_with_status = [
        {"lesson": lesson, "is_completed": lesson.id in completed_ids}
        for lesson in lessons
    ]
    return render(request, "lessons/lesson_list.html", {"lessons_with_status": lessons_with_status})


@login_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    is_completed = Completion.objects.filter(user=request.user, lesson=lesson).exists()

    if request.method == "POST" and "mark_complete" in request.POST:
        Completion.objects.get_or_create(user=request.user, lesson=lesson)
        return redirect("lessons:quiz", pk=lesson.pk)

    return render(request, "lessons/lesson_detail.html", {
        "lesson": lesson,
        "is_completed": is_completed,
    })


@login_required
def lesson_quiz(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if not Completion.objects.filter(user=request.user, lesson=lesson).exists():
        return redirect("lessons:detail", pk=lesson.pk)

    questions = lesson.questions.all()
    if not questions:
        return redirect("lessons:list")

    # Once a question has an attempt, it's locked in permanently — no retries.
    existing_attempts = {
        a.question_id: a
        for a in QuizAttempt.objects.filter(user=request.user, question__lesson=lesson)
    }
    already_answered = len(existing_attempts) == questions.count()

    if request.method == "POST" and not already_answered:
        for question in questions:
            if question.id in existing_attempts:
                continue  # already locked in, skip re-grading it
            choice_id = request.POST.get(f"question_{question.id}")
            if not choice_id:
                continue
            choice = get_object_or_404(question.choices, pk=choice_id)
            attempt = QuizAttempt.objects.create(
                user=request.user,
                question=question,
                selected_choice=choice,
                is_correct=choice.is_correct,
            )
            existing_attempts[question.id] = attempt
        already_answered = len(existing_attempts) == questions.count()

    return render(request, "lessons/lesson_quiz.html", {
        "lesson": lesson,
        "questions": questions,
        "existing_attempts": existing_attempts,
        "quiz_already_answered": already_answered,
    })