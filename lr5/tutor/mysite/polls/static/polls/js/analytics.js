document.addEventListener('DOMContentLoaded', function() {
    const analyticsData = document.getElementById('analyticsData');
    const chartContainer = document.getElementById('chartContainer');
    const showBarChart = document.getElementById('showBarChart');
    const showPieChart = document.getElementById('showPieChart');
    const showInteractiveChart = document.getElementById('showInteractiveChart');
    const exportJsonBtn = document.getElementById('exportJsonBtn');
    const exportCsvBtn = document.getElementById('exportCsvBtn');

    // Загрузка данных аналитики
    loadAnalyticsData();

    // Обработчики кнопок графиков
    showBarChart.addEventListener('click', () => loadChart('bar'));
    showPieChart.addEventListener('click', () => loadChart('pie'));
    showInteractiveChart.addEventListener('click', () => loadChart('interactive'));

    // Обработчики экспорта
    exportJsonBtn.addEventListener('click', () => exportPoll('json'));
    exportCsvBtn.addEventListener('click', () => exportPoll('csv'));

    // Загрузка данных аналитики
    function loadAnalyticsData() {
        fetch(`/analytics/api/stats/?question_id=${questionId}`)
            .then(response => response.json())
            .then(stats => {
                displayAnalyticsData(stats);
            })
            .catch(error => {
                console.error('Error:', error);
                analyticsData.innerHTML = `
                    <div class="alert alert-danger">
                        Ошибка при загрузке данных: ${error.message}
                    </div>
                `;
            });
    }

    // Отображение данных аналитики
    function displayAnalyticsData(stats) {
        if (!stats || stats.error) {
            analyticsData.innerHTML = `
                <div class="alert alert-warning">
                    Не удалось загрузить данные аналитики
                </div>
            `;
            return;
        }

        let choicesHtml = '';
        stats.choices_stats.forEach(choice => {
            choicesHtml += `
                <tr>
                    <td>${choice.choice_text}</td>
                    <td>${choice.votes}</td>
                    <td>
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar" role="progressbar"
                                 style="width: ${choice.percentage}%"
                                 aria-valuenow="${choice.percentage}"
                                 aria-valuemin="0"
                                 aria-valuemax="100">
                                ${choice.percentage}%
                            </div>
                        </div>
                    </td>
                </tr>
            `;
        });

        analyticsData.innerHTML = `
            <div class="mb-4">
                <h4>${stats.question_text}</h4>
                <p class="text-muted">
                    <i class="bi bi-calendar"></i>
                    Дата создания: ${new Date(stats.pub_date).toLocaleDateString()}
                    | <i class="bi bi-person-check"></i>
                    Всего голосов: <strong>${stats.total_votes}</strong>
                </p>
            </div>

            <h5>Детальная статистика:</h5>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Вариант ответа</th>
                            <th>Голосов</th>
                            <th>Процент</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${choicesHtml}
                    </tbody>
                </table>
            </div>
        `;
    }

    // Загрузка графика
    function loadChart(chartType) {
        fetch(`/analytics/api/charts/?question_id=${questionId}&type=${chartType}`)
            .then(response => response.json())
            .then(data => {
                displayChart(data);
            })
            .catch(error => {
                console.error('Error:', error);
                chartContainer.innerHTML = `
                    <div class="alert alert-danger">
                        Ошибка при загрузке графика: ${error.message}
                    </div>
                `;
            });
    }

    // Отображение графика
    function displayChart(chartData) {
        if (chartData.chart_type === 'interactive' && chartData.chart_data) {
            chartContainer.innerHTML = `
                <div id="interactiveChart" style="width: 100%; height: 300px;"></div>
            `;

            Plotly.newPlot('interactiveChart', chartData.chart_data.data, chartData.chart_data.layout);

        } else if (chartData.image_base64) {
            chartContainer.innerHTML = `
                <div class="text-center">
                    <img src="data:image/png;base64,${chartData.image_base64}"
                         class="img-fluid" alt="Chart">
                </div>
            `;
        } else if (chartData.svg) {
            chartContainer.innerHTML = `
                <div id="svgContainer">${chartData.svg}</div>
            `;
        }
    }

    // Экспорт данных
    function exportPoll(format) {
        window.open(`/analytics/api/export/?question_id=${questionId}&format=${format}`, '_blank');
    }
});