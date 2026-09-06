from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lesson, Completion, Choice, Question, QuizAttempt, OpenQuestion
from django.http import JsonResponse
from .templatetags.lessons_extras import split_into_sections, build_lesson_pages

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

    pages = build_lesson_pages(lesson)
    toc = []
    seen_headings = set()
    for index, page in enumerate(pages):
        label = page["heading"] if page["heading"] else "Overview"
        if label not in seen_headings:
            toc.append({"label": label, "index": index, "level": page["level"] if page["heading"] else 2})
            seen_headings.add(label)

    return render(request, "lessons/lesson_detail.html", {
        "lesson": lesson,
        "is_completed": is_completed,
        "toc": toc,
    })



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
    pages = build_lesson_pages(lesson)

    if section_index < 0 or section_index >= len(pages):
        return redirect("lessons:detail", pk=lesson.pk)

    page = pages[section_index]
    current_label = page["heading"] if page["heading"] else "Overview"

    toc = []
    seen_headings = set()
    for index, p in enumerate(pages):
        label = p["heading"] if p["heading"] else "Overview"
        if label not in seen_headings:
            toc.append({
                "label": label,
                "index": index,
                "level": p["level"] if p["heading"] else 2,
                "is_current": label == current_label,
            })
            seen_headings.add(label)

    existing_attempts = {
        a.question_id: a
        for a in QuizAttempt.objects.filter(user=request.user, question__lesson=lesson)
    }

    return render(request, "lessons/lesson_section.html", {
        "lesson": lesson,
        "page": page,
        "existing_attempts": existing_attempts,
        "section_index": section_index,
        "total_sections": len(pages),
        "has_prev": section_index > 0,
        "has_next": section_index < len(pages) - 1,
        "toc": toc,
    })