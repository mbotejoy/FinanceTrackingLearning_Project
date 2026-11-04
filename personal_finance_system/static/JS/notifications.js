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

    const closeButton = document.getElementById(
        "closeNotification"
    );

    const classificationData = document.getElementById(
        "classificationAlertData"
    );

    if (
        !notification ||
        !titleElement ||
        !messageElement ||
        !closeButton ||
        !classificationData
    ) {
        return;
    }

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

    const alert = messages[classification];

    if (!alert) return;

    titleElement.textContent = alert.title;
    messageElement.textContent = alert.message;

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