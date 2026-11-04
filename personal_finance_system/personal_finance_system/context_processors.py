from .classification_service import classify_student_spending
from datetime import date

def spending_classification(request):
    if not request.user.is_authenticated:
        return {}

    if getattr(request.user, "role", None) == "admin":
        return {}

    today = date.today()

    spending_analysis = classify_student_spending(
        request.user,
        today.year,
        today.month
    )

    return {
        "global_spending_analysis": spending_analysis
    }