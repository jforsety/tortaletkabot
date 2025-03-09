document.addEventListener('DOMContentLoaded', function() {
    const rawData = JSON.parse(document.getElementById('chart-data').textContent);

    const config = {
        type: 'bar',
        data: {
            labels: rawData.labels,
            datasets: [{
                label: 'Активные пользователи',
                data: rawData.counts,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0,
                        stepSize: 1
                    }
                }
            }
        }
    };

    const ctx = document.getElementById('activityChart');
    if (ctx) {
        new Chart(ctx, config);
    }
});