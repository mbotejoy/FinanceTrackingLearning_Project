from .models import Notification

def finance_notifications(request):
    if not request.user.is_authenticated:
        return {
            "unread_notification_count": 0,
        }

    if (
        getattr(request.user, "role", None) == "admin"
        and request.user.is_staff
    ):
        return {
            "unread_notification_count": 0,
        }

    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return {
        "unread_notification_count": unread_count,
    }