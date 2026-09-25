document.addEventListener("DOMContentLoaded", function () {
    const eyeIcon = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
    const eyeOffIcon = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="m3 3 18 18M10.6 6.2A10.8 10.8 0 0 1 12 6c6.5 0 10 6 10 6a17.4 17.4 0 0 1-3.2 3.9M6.2 6.3C3.5 8.1 2 12 2 12s3.5 6 10 6a10.8 10.8 0 0 0 3.4-.5"></path><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"></path></svg>';

    document.querySelectorAll(".password-toggle").forEach(function (toggle) {
        const input = document.getElementById(toggle.dataset.target);

        if (!input) {
            return;
        }

        toggle.addEventListener("click", function () {
            const isHidden = input.type === "password";

            input.type = isHidden ? "text" : "password";
            toggle.setAttribute("aria-label", isHidden ? "Hide password" : "Show password");
            toggle.innerHTML = isHidden ? eyeOffIcon : eyeIcon;
            input.focus();
        });
    });
});
