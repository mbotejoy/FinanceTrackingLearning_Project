document.addEventListener("DOMContentLoaded", function () {
    const notification = document.getElementById(
        "recommendationNotification"
    );

    const titleElement = document.getElementById("notificationTitle");
    const messageElement = document.getElementById("notificationMessage");
    const closeButton = document.getElementById("closeNotification");

    if (!notification || !titleElement || !messageElement || !closeButton) {
        return;
    }

    const savedNotification = sessionStorage.getItem(
        "financeWiseNotification"
    );

    if (!savedNotification) {
        return;
    }

    try {
        const alertData = JSON.parse(savedNotification);

        titleElement.textContent = alertData.title;
        messageElement.textContent = alertData.message;

        notification.hidden = false;

        function hideNotification() {
            notification.hidden = true;

            sessionStorage.removeItem("financeWiseNotification");
        }

        const notificationTimer = setTimeout(
            hideNotification,
            8000
        );

        closeButton.addEventListener("click", function () {
            clearTimeout(notificationTimer);
            hideNotification();
        });

    } catch (error) {
        console.error("Could not display notification:", error);

        sessionStorage.removeItem("financeWiseNotification");
    }
});
