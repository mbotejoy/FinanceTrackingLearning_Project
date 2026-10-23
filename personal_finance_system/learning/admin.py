from django.contrib import admin
from .models import LearningContent, QuizQuestion

@admin.register(LearningContent)
class LearningContentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "is_published",
    )
    list_filter = ("topic", "is_published")
    search_fields = ("title",)
    list_editable = ("is_published",)


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "question_text",
        "topic",
        "correct_answer",
        "is_published",
    )

    list_filter = ("topic", "is_published")
    search_fields = ("question_text",)
    list_editable = ("is_published",)
