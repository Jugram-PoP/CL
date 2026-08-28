from django.contrib.auth.decorators import login_required
from .templatetags.lessons_extras import split_into_sections
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lesson, Completion, Choice, Question, QuizAttempt, OpenQuestion
from django.http import JsonResponse



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
        return redirect("lessons:detail", pk=lesson.pk)

    sections = split_into_sections(lesson.content)
    questions_by_section = {}
    for q in lesson.questions.all():
        questions_by_section.setdefault(q.section, []).append(q)

    existing_attempts = {
        a.question_id: a
        for a in QuizAttempt.objects.filter(user=request.user, question__lesson=lesson)
    }

    section_data = []
    for heading, html in sections:
        section_data.append({
            "heading": heading,
            "html": html,
            "questions": questions_by_section.get(heading, []),
        })

    return render(request, "lessons/lesson_detail.html", {
        "lesson": lesson,
        "is_completed": is_completed,
        "sections": section_data,
        "existing_attempts": existing_attempts,
    })

from django.http import JsonResponse

@login_required
def answer_question(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)
    choice = get_object_or_404(Choice, pk=request.POST.get("choice_id"))
    question = choice.question
    attempt, created = QuizAttempt.objects.get_or_create(
        user=request.user,
        question=question,
        defaults={"selected_choice": choice, "is_correct": choice.is_correct},
    )
    return JsonResponse({
        "is_correct": attempt.is_correct,
        "already_answered": not created,
    })

@login_required
def lesson_section(request, pk, section_index):
    lesson = get_object_or_404(Lesson, pk=pk)
    sections = split_into_sections(lesson.content)

    if section_index < 0 or section_index >= len(sections):
        return redirect("lessons:detail", pk=lesson.pk)

    heading, html = sections[section_index]
    questions = lesson.questions.filter(section=heading)
    open_questions = lesson.open_questions.filter(section=heading)

    existing_attempts = {
        a.question_id: a
        for a in QuizAttempt.objects.filter(user=request.user, question__lesson=lesson)
    }

    return render(request, "lessons/lesson_section.html", {
        "lesson": lesson,
        "heading": heading,
        "html": html,
        "questions": questions,
        "open_questions": open_questions,
        "existing_attempts": existing_attempts,
        "section_index": section_index,
        "total_sections": len(sections),
        "has_prev": section_index > 0,
        "has_next": section_index < len(sections) - 1,
        "is_last": section_index == len(sections) - 1,
    })