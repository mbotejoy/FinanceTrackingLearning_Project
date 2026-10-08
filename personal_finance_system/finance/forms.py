from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name", "type"]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Enter category name"
            }),
            "type": forms.Select()
        }