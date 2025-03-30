document.addEventListener('DOMContentLoaded', function() {
    try {
        const chartDataElement = document.getElementById('chart-data');
        if (!chartDataElement) {
            throw new Error('Chart data element not found');
        }

        const rawData = JSON.parse(chartDataElement.textContent);
        console.log('Loaded chart data:', rawData);

        const config = {
            type: 'bar',
            data: {
                labels: rawData.labels,
                datasets: [{
                    label: 'Активные пользователи',
                    data: rawData.counts.map(Number),
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
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Пользователей: ${context.raw}`;
                            }
                        }
                    }
                }
            }
        };

        const ctx = document.getElementById('activityChart');
        if (ctx) {
            new Chart(ctx, config);
        } else {
            console.warn('Canvas element not found');
        }
    } catch (error) {
        console.error('Error initializing chart:', error);
    }
});