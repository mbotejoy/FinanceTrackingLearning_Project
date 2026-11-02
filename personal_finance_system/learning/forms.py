from django import forms
from .models import LearningContent, QuizQuestion

# This form allows administrators to add and edit lessons using the same fields defined in the model.
class LearningContentForm(forms.ModelForm):

    class Meta:
        model = LearningContent

        fields = [
            "title",
            "topic",
            "description",
            "content",
            "is_published",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Enter lesson title"
            }),
            "topic": forms.Select(),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Enter a short description"
            }),
            "content": forms.Textarea(attrs={
                "rows": 12,
                "placeholder": "Write the lesson here"
            }),
        }

class QuizQuestionForm(forms.ModelForm):

    class Meta:
        model = QuizQuestion
        fields = [
            "topic",
            "question_text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_answer",
            "explanation",
            "is_published",
        ]

        widgets = {
            "question_text": forms.Textarea(attrs={"rows": 3}),
            "explanation": forms.Textarea(attrs={"rows": 3}),
        }