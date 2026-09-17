document.addEventListener("DOMContentLoaded", function () {

    const nextButton = document.getElementById("nextQuestion");
    const previousButton = document.getElementById("previousQuestion");

    if (nextButton) {

        nextButton.addEventListener("click", function () {

            console.log("Moving to next question");

        });

    }


    if (previousButton) {

        previousButton.addEventListener("click", function () {

            console.log("Moving to previous question");

        });

    }

});