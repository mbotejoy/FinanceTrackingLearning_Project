
document.addEventListener("DOMContentLoaded", function () {

    const dataElement = document.getElementById(
        "spending-trend-data"
    );

    const canvas = document.getElementById(
        "spendingTrendChart"
    );

    if (!dataElement || !canvas) return;

    const spendingData = JSON.parse(dataElement.textContent);

    new Chart(canvas, {
        type: "line",

        data: {
            labels: spendingData.map(item => item.label),

            datasets: [{
                label: "Monthly Spending (KES)",
                data: spendingData.map(item => item.total),

                borderColor: "#2878B5",
                backgroundColor: "rgba(40, 120, 181, 0.12)",

                borderWidth: 3,
                fill: true,
                tension: 0.35,

                pointRadius: 5,
                pointBackgroundColor: "#2878B5"
            }]
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

                    title: {
                        display: true,
                        text: "Amount Spent (KES)"
                    }
                },

                x: {
                    title: {
                        display: true,
                        text: "Month"
                    }
                }
            }
        }
    });

});
