from django.contrib import admin
from .models import Lesson, Completion, Question, Choice, QuizAttempt, OpenQuestion

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "lesson", "section")
    search_fields = ("text", "section")
    inlines = [ChoiceInline]

class LessonAdmin(admin.ModelAdmin):
    list_display = ("title","order")
    search_fields = ("title",)
    inlines = [QuestionInline]

class CompletionAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed_at")
    list_filter = ("lesson",)

admin.site.register(Completion, CompletionAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizAttempt)
admin.site.register(OpenQuestion)

