from django import forms
from .models import LearningContent

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