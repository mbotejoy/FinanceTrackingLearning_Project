from django.utils import timezone
from personal_finance_system.classification_service import classify_student_spending
from .models import Notification
from learning.models import LearningContent

def finance_notifications(request):

    if not request.user.is_authenticated:
        return {
            "unread_notification_count": 0,
            "classification_alert": None
        }

    if (
        getattr(request.user, "role", None) == "admin"
        and request.user.is_staff
    ):
        return {
            "unread_notification_count": 0,
            "classification_alert": None
        }

    today = timezone.localdate()
    period_key = today.strftime("%Y-%m")

    # Get the user's current spending classification.
    spending_analysis = classify_student_spending(
        user=request.user,
        year=today.year,
        month=today.month
    )

    classification = (
        spending_analysis.get("classification")
        if spending_analysis
        else None
    )

    classification_alert = None

    # Only generate an alert when a valid classification exists.
    if classification:

        alert_messages = {
            "Low": (
                "Low Spending Behaviour",
                "You are managing your spending well. "
                "Keep maintaining your financial discipline.",
                "success"
            ),
            "Moderate": (
                "Moderate Spending Behaviour",
                "Your spending is moderate. Review your expenses "
                "to maintain a healthy financial balance.",
                "info"
            ),
            "High": (
                "High Spending Behaviour",
                "Your spending is high. Consider reducing "
                "unnecessary expenses and reviewing your budget.",
                "warning"
            )
        }

        title, message, notification_type = alert_messages.get(
            classification,
            (None, None, None)
        )

        if title:

            notification = Notification.objects.filter(
                user=request.user,
                rule_key="spending_classification",
                is_active=True
            ).first()

            # Create the first classification notification.
            if notification is None:

                notification = Notification.objects.create(
                    user=request.user,
                    rule_key="spending_classification",
                    period_key=period_key,
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    is_active=True,
                    is_read=False
                )

                classification_alert = {
                    "classification": classification
                }

            # Generate a new alert only when the classification changes.
            elif notification.title != title:

                notification.title = title
                notification.message = message
                notification.notification_type = notification_type
                notification.period_key = period_key
                notification.is_read = False

                notification.save(
                    update_fields=[
                        "title",
                        "message",
                        "notification_type",
                        "period_key",
                        "is_read"
                    ]
                )

                classification_alert = {
                    "classification": classification
                }

    else:
        # Deactivate an old classification notification if
        # the user no longer has a valid classification.
        Notification.objects.filter(
            user=request.user,
            rule_key="spending_classification",
            is_active=True
        ).update(
            is_active=False,
            resolved_at=timezone.now()
        )

    # Connect existing financial recommendations to relevant lessons.
    topic_by_rule = {
        "expenses_exceed_income": "spending",
        "high_expense_ratio": "spending",
        "moderate_expense_ratio": "spending",
        "budget_exceeded": "budgeting",
        "budget_nearly_exhausted": "budgeting",
        "no_income_recorded": "budgeting",
        "no_active_savings_goal": "saving",
        "savings_goal_reached": "saving",
        "savings_goal_target_date_passed": "saving",
        "savings_goal_approaching": "saving",
    }

    active_financial_notifications = Notification.objects.filter(
        user=request.user,
        is_active=True
    ).exclude(
        rule_key="spending_classification"
    ).exclude(
        rule_key__startswith="lesson_"
    )

    recommended_topics = {
        topic_by_rule[notification.rule_key]
        for notification in active_financial_notifications
        if notification.rule_key in topic_by_rule
    }

    current_lesson_keys = set()

    for topic in recommended_topics:
        lesson = LearningContent.objects.filter(
            topic=topic,
            is_published=True
        ).order_by("-created_at").first()

        if lesson is None:
            continue

        lesson_key = f"lesson_{lesson.id}"
        current_lesson_keys.add(lesson_key)

        lesson_notification = Notification.objects.filter(
            user=request.user,
            rule_key=lesson_key
        ).first()

        title = f"Recommended lesson: {lesson.title}"
        message = (
            "Based on your recent financial activity, "
            "this lesson may help you improve your financial decisions."
        )

        if lesson_notification is None:
            Notification.objects.create(
                user=request.user,
                rule_key=lesson_key,
                title=title,
                message=message,
                notification_type="info",
                period_key=period_key,
                is_active=True,
                is_read=False
            )

        elif not lesson_notification.is_active:
            lesson_notification.title = title
            lesson_notification.message = message
            lesson_notification.notification_type = "info"
            lesson_notification.period_key = period_key
            lesson_notification.is_active = True
            lesson_notification.is_read = False
            lesson_notification.resolved_at = None
            lesson_notification.save()

        elif (
            lesson_notification.title != title
            or lesson_notification.message != message
        ):
            lesson_notification.title = title
            lesson_notification.message = message
            lesson_notification.save(
                update_fields=["title", "message"]
            )

    # Deactivate lesson notifications that are no longer relevant.
    old_lesson_notifications = Notification.objects.filter(
        user=request.user,
        rule_key__startswith="lesson_",
        is_active=True
    )

    for old_notification in old_lesson_notifications:
        if old_notification.rule_key not in current_lesson_keys:
            old_notification.is_active = False
            old_notification.resolved_at = timezone.now()
            old_notification.save(
                update_fields=["is_active", "resolved_at"]
            )
        
    # Count active unread notifications.
    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False,
        is_active=True
    ).count()

    lesson_alert = Notification.objects.filter(
    user=request.user,
    rule_key__startswith="lesson_",
    is_active=True,
    is_read=False
    ).order_by("-created_at").first()


    return {
        "unread_notification_count": unread_count,
        "classification_alert": classification_alert,
        "lesson_alert": lesson_alert
    }