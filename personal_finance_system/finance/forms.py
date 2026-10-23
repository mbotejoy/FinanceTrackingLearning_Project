
from django import forms
from .models import Category, Transaction, Budget, SavingsGoal


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


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction

        fields = [
            "amount",
            "type",
            "category",
            "date",
            "description",
        ]

        widgets = {
            "amount": forms.NumberInput(attrs={
                "step": "0.01",
                "min": "0.01",
                "placeholder": "Enter amount"
            }),
            "type": forms.Select(),
            "category": forms.Select(),
            "date": forms.DateInput(attrs={
                "type": "date"
            }),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Enter a short description"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = (
            Category.objects.all().order_by("name")
        )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= 0:
            raise forms.ValidationError(
                "Amount must be greater than zero."
            )

        return amount

    def clean(self):
        cleaned_data = super().clean()

        transaction_type = cleaned_data.get("type")
        category = cleaned_data.get("category")

        if category and transaction_type != category.type:
            self.add_error(
                "category",
                "Select a category matching the transaction type."
            )

        return cleaned_data


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget

        fields = [
            "name",
            "category",
            "amount",
            "start_date",
            "end_date",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "e.g. Monthly Food Budget"
            }),
            "category": forms.Select(),
            "amount": forms.NumberInput(attrs={
                "step": "0.01",
                "min": "0.01",
                "placeholder": "Enter amount"
            }),
            "start_date": forms.DateInput(attrs={
                "type": "date"
            }),
            "end_date": forms.DateInput(attrs={
                "type": "date"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = (
            Category.objects.filter(
                type="expense"
            ).order_by("name")
        )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= 0:
            raise forms.ValidationError(
                "Budget amount must be greater than zero."
            )

        return amount

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            self.add_error(
                "end_date",
                "End date cannot be before the start date."
            )

        return cleaned_data

class SavingsGoalForm(forms.ModelForm):
    status = forms.ChoiceField(
    choices=SavingsGoal.STATUS_CHOICES,
    required=False
)

    class Meta:
        model = SavingsGoal

        fields = [
            "name",
            "target_amount",
            "current_amount",
            "target_date",
            "status",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "e.g. New laptop"
            }),

            "target_amount": forms.NumberInput(attrs={
                "min": "0.01",
                "step": "0.01",
                "placeholder": "Enter your target amount"
            }),

            "current_amount": forms.NumberInput(attrs={
                "min": "0",
                "step": "0.01",
                "placeholder": "Amount saved so far"
            }),

            "target_date": forms.DateInput(attrs={
                "type": "date"
            }),

            "status": forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()

        target = cleaned_data.get("target_amount")
        current = cleaned_data.get("current_amount")

        if target is not None and target <= 0:
            self.add_error(
                "target_amount",
                "Your savings target must be greater than zero."
            )

        if current is not None and current < 0:
            self.add_error(
                "current_amount",
                "The amount saved cannot be negative."
            )

        if target is not None and current is not None and current > target:
            self.add_error(
                "current_amount",
                "The amount saved cannot exceed the target amount."
            )

        return cleaned_data
