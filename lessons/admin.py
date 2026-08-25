from django.contrib import admin
from .models import Lesson, Completion, Question, Choice, QuizAttempt

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Completion)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizAttempt)