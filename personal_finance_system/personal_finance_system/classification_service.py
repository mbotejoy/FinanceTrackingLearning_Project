# This service loads your saved model, prepares the 
# input features and returns a classification.


from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
from django.conf import settings


MODEL_DIR = Path(settings.BASE_DIR) / "saved_models"

# Map FinanceWise category names to notebook categories.
# Add or adjust names to match your database.
CATEGORY_MAPPING = {
    "rent": "housing",
    "housing": "housing",
    "groceries": "food",
    "food": "food",
    "meals": "food",
    "transport": "transportation",
    "transportation": "transportation",
    "matatu": "transportation",
    "books": "books_supplies",
    "stationery": "books_supplies",
    "books & supplies": "books_supplies",
    "entertainment": "entertainment",
    "personal care": "personal_care",
    "technology": "technology",
    "internet": "technology",
    "health": "health_wellness",
    "medical": "health_wellness",
    "miscellaneous": "miscellaneous",
    "other": "miscellaneous",
    "tuition": None,
}


@lru_cache(maxsize=1)
def load_classifier():
    model = joblib.load(
        MODEL_DIR / "spending_classifier_ratio_based.pkl"
    )
    config = joblib.load(
        MODEL_DIR / "spending_classifier_ratio_config.pkl"
    )
    return model, config


def classify_student_spending(user, year, month):
    from django.db.models import Sum
    from finance.models import Transaction

    model, config = load_classifier()

    transactions = Transaction.objects.filter(
        user=user,
        date__year=year,
        date__month=month,
    ).select_related("category")

    income = transactions.filter(
        type="income"
    ).aggregate(total=Sum("amount"))["total"] or 0

    if income <= 0:
        return {
            "classification": None,
            "message": "Record your monthly income to view your classification."
        }

    expenses = {
        name: 0.0
        for name in config["expense_columns"]
    }

    unmapped = set()

    for transaction in transactions.filter(type="expense"):
        category_name = (
            transaction.category.name.strip().lower()
            if transaction.category else ""
        )

        if category_name not in CATEGORY_MAPPING:
            unmapped.add(category_name or "Uncategorised")
            continue

        mapped_name = CATEGORY_MAPPING[category_name]

        # Tuition is excluded from this model.
        if mapped_name is None:
            continue

        expenses[mapped_name] += float(transaction.amount)

    if unmapped:
        return {
            "classification": None,
            "message": "Some expense categories need mapping.",
            "unmapped_categories": sorted(unmapped),
        }

    total_expenses = sum(expenses.values())

    if total_expenses <= 0:
        return {
            "classification": None,
            "message": "Record expenses to view your classification."
        }

    if any(value < 0 for value in expenses.values()):
        return {
            "classification": None,
            "message": "Expense amounts must not be negative."
        }

    features = {
        "spending_ratio": total_expenses / float(income)
    }

    for name in config["expense_columns"]:
        features[f"{name}_proportion"] = (
            expenses[name] / total_expenses
        )

    X = pd.DataFrame(
        [features],
        columns=config["feature_columns"]
    )

    prediction = str(model.predict(X)[0])

    return {
        "classification": prediction,
        "spending_ratio": round(features["spending_ratio"], 3),
        "monthly_income": float(income),
        "monthly_expenses": round(total_expenses, 2),
        "message": "Classification successful",
    }
