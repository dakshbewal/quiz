from django.contrib import admin
from .models import Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'correct_answer')
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
