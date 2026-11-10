
document.addEventListener("DOMContentLoaded", function () {

    const notification = document.getElementById(
        "recommendationNotification"
    );

    const titleElement = document.getElementById(
        "notificationTitle"
    );

    const messageElement = document.getElementById(
        "notificationMessage"
    );

    const notificationLink = document.getElementById(
        "notificationLink"
    );

    const closeButton = document.getElementById(
        "closeNotification"
    );

    const classificationData = document.getElementById(
        "classificationAlertData"
    );

    const lessonData = document.getElementById(
        "lessonAlertData"
    );

    if (
        !notification ||
        !titleElement ||
        !messageElement ||
        !closeButton
    ) {
        return;
    }

    let alert = null;
    let linkUrl = null;
    let linkText = "View All Recommendations";

    // 1. Check for a lesson recommendation first.
    if (lessonData) {

        const lessonId = lessonData.dataset.lessonId;

        alert = {
            title: lessonData.dataset.title,
            message: lessonData.dataset.message
        };

        linkUrl = `/learning/${lessonId}/`;
        linkText = "View Recommended Lesson";

    }

    // 2. Otherwise, display the spending classification alert.
    else if (classificationData) {

        const classification =
            classificationData.dataset.classification;

        const messages = {
            "Low": {
                title: "Low Spending Behaviour",
                message: "You are managing your spending well. Keep maintaining your financial discipline."
            },

            "Moderate": {
                title: "Moderate Spending Behaviour",
                message: "Your spending is moderate. Review your expenses to maintain a healthy financial balance."
            },

            "High": {
                title: "High Spending Behaviour",
                message: "Your spending is high. Consider reducing unnecessary expenses and reviewing your budget."
            }
        };

        alert = messages[classification];
        linkUrl = notificationLink
            ? notificationLink.href
            : null;
    }

    if (!alert) {
        return;
    }

    titleElement.textContent = alert.title;
    messageElement.textContent = alert.message;

    if (notificationLink && linkUrl) {
        notificationLink.href = linkUrl;
        notificationLink.textContent = linkText;
    }

    notification.hidden = false;

    function hideNotification() {
        notification.hidden = true;
    }

    const timer = setTimeout(hideNotification, 8000);

    closeButton.addEventListener("click", function () {
        clearTimeout(timer);
        hideNotification();
    });

});
