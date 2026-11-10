
document.addEventListener("DOMContentLoaded", function () {

    // Retrieve registration chart data from Django
    const registrationLabels = JSON.parse(
        document.getElementById("registration-labels").textContent
    );

    const registrationDatasets = JSON.parse(
        document.getElementById("registration-datasets").textContent
    );

    // Retrieve quiz activity data from Django
    const quizLabels = JSON.parse(
        document.getElementById("quiz-labels").textContent
    );

    const quizDatasets = JSON.parse(
        document.getElementById("quiz-datasets").textContent
    );

    // User Registration Chart
    const registrationCanvas = document.getElementById("registrationChart");

    if (registrationCanvas) {
        new Chart(registrationCanvas, {
            type: "bar",
            data: {
                labels: registrationLabels,
                datasets: registrationDatasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "top"
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        },
                        title: {
                            display: true,
                            text: "Number of Registered Users"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: "Month and Year"
                        }
                    }
                }
            }
        });
    }

    // Monthly Quiz Attempts Chart
    const quizCanvas = document.getElementById("quizActivityChart");

    if (quizCanvas) {
        new Chart(quizCanvas, {
            type: "line",
            data: {
                labels: quizLabels,
                datasets: quizDatasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "top"
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        },
                        title: {
                            display: true,
                            text: "Number of Quiz Attempts"
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: "Month and Year"
                        }
                    }
                }
            }
        });
    }
    
    const dataElement = document.getElementById(
        "spending-category-data"
    );

    if (!dataElement) return;

    const categories = JSON.parse(dataElement.textContent);

    if (categories.length === 0) return;

    const labels = categories.map(item => item.name);

    const amounts = categories.map(item => item.total_spent);

    const percentages = categories.map(item => item.percentage);

    // Bar Chart: Total expenditure by category
    const spendingCanvas = document.getElementById(
        "spendingCategoryChart"
    );

    if (spendingCanvas) {
        new Chart(spendingCanvas, {
            type: "bar",

            data: {
                labels: labels,
                datasets: [{
                    label: "Total Expenditure (KES)",
                    data: amounts,
                    backgroundColor: [
                        "#4F46E5",
                        "#0D9488",
                        "#F59E0B",
                        "#EC4899",
                        "#3B82F6",
                        "#8B5CF6",
                        "#14B8A6"
                    ],
                    borderRadius: 5
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Amount Spent (KES)"
                        }
                    }
                }
            }
        });
    }

    // Doughnut Chart: Percentage expenditure
    const percentageCanvas = document.getElementById(
        "spendingPercentageChart"
    );

    if (percentageCanvas) {
        new Chart(percentageCanvas, {
            type: "doughnut",

            data: {
                labels: labels,
                datasets: [{
                    data: percentages,
                    backgroundColor: [
                        "#4F46E5",
                        "#0D9488",
                        "#F59E0B",
                        "#EC4899",
                        "#3B82F6",
                        "#8B5CF6",
                        "#14B8A6"
                    ]
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }


});
