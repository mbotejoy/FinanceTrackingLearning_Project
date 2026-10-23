
document.addEventListener("DOMContentLoaded", function () {
    const questions = Array.from(
        document.querySelectorAll(".quiz-question")
    );

    if (questions.length === 0) {
        return;
    }

    const previousButton = document.getElementById("previousQuestion");
    const nextButton = document.getElementById("nextQuestion");
    const submitButton = document.getElementById("submitQuiz");
    const counter = document.getElementById("questionCounter");
    const form = document.getElementById("quizForm");

    let currentIndex = 0;

    function showQuestion(index) {
        questions.forEach(function (question, position) {
            question.hidden = position !== index;
        });

        currentIndex = index;

        counter.textContent =
            `Question ${currentIndex + 1} of ${questions.length}`;

        previousButton.disabled = currentIndex === 0;

        const isLastQuestion = currentIndex === questions.length - 1;

        nextButton.hidden = isLastQuestion;
        submitButton.hidden = !isLastQuestion;
    }

    previousButton.addEventListener("click", function () {
        if (currentIndex > 0) {
            showQuestion(currentIndex - 1);
        }
    });

    nextButton.addEventListener("click", function () {
        if (currentIndex < questions.length - 1) {
            showQuestion(currentIndex + 1);
        }
    });

    form.addEventListener("submit", function (event) {
        const unanswered = questions.some(function (question) {
            return !question.querySelector('input[type="radio"]:checked');
        });

        if (unanswered) {
            event.preventDefault();
            alert("Please answer every question before submitting.");
        }
    });

    showQuestion(0);
});
