from django.utils import timezone
from personal_finance_system.classification_service import classify_student_spending
from .models import Notification

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

    # Count active unread notifications.
    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False,
        is_active=True
    ).count()

    return {
        "unread_notification_count": unread_count,
        "classification_alert": classification_alert
    }