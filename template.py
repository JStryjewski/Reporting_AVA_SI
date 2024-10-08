# template.py
html_template = """
<!DOCTYPE html> 
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raport Dostępności</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }
        .header {
            background-color: rgb(126, 186, 0);
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            flex-wrap: wrap;
        }
        .header h1 {
            margin: 0;
            flex: 1;
            text-align: center;
            font-size: 42px;
        }
        .header .date {
            flex: 0 1 auto;
            font-size: 24px;
            white-space: nowrap;  /* Prevents the date from wrapping */
        }
        .header img {
            height: 100px;
            flex: 0 1 auto;
        }

        @media screen and (max-width: 768px) {
            .header h1 {
                font-size: 28px;
            }
            .header .date {
                font-size: 18px;
            }
            .header img {
                height: 40px;
            }
        }

        @media screen and (max-width: 480px) {
            .header {
                flex-direction: column; /* Stack date, title, and logo on top of each other on mobile */
                text-align: center;
            }
            .header h1 {
                font-size: 24px; 
            }
            .header .date {
                font-size: 16px;
                margin-bottom: 10px;
            }
            .header img {
                height: 35px;
                margin-top: 10px;
            }
        }

        h2 {
            text-align: center;
            flex-grow: 1;
            color: rgb(126, 186, 0);
            font-size: 32px; 
            margin: 20px 0;
        }
         
        @media screen and (max-width: 768px) {
            h2 {
                font-size: 24px; 
            }
        }

        @media screen and (max-width: 480px) {
            h2 {
                font-size: 18px; 
            }
        }
         
        .charts {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            margin-top: 50px;
        }

        .chart-container {
            width: 300px;
            text-align: center;
            margin-bottom: 30px;
        }

        .chart-title {
            font-size: 24px;
            margin-bottom: 10px;
        }

        /* Media queries to adjust chart sizes and layout */
        @media screen and (max-width: 1024px) {
            .chart-container {
                width: 200px; 
            }
            .chart-title {
                font-size: 20px;
            }
        }

        @media screen and (max-width: 768px) {
            .chart-container {
                width: 150px; 
            }
            .chart-title {
                font-size: 18px;
            }
        }

        @media screen and (max-width: 480px) {
            .chart-container {
                width: 120px; 
            }
            .chart-title {
                font-size: 16px;
            }
        }

        .buttons {
            text-align: center;
            margin-top: 20px;
        }

        .buttons button {
            text-align: center;
            font-size: 24px;
        }

        @media screen and (max-width: 768px) {
            .buttons button {
                font-size: 16px; 
            }
        }

        @media screen and (max-width: 480px) {
            .buttons button {
                font-size: 14px;
            }
        }

        .line-chart-container {
            margin: 50px auto;
            width: 80%;
        }

        .charts {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }
        .chart-container {
            flex: 0 1 10%; /* Ensures a maximum of 5 charts in one line */
            margin: 10px;
        }

        @media screen and (max-width: 768px) {
            .chart-container {
                flex: 0 1 10%; 
            }
        }

        @media screen and (max-width: 480px) {
            .chart-container {
                flex: 0 1 50%; 
            }
        }

        table {
            width: 100%;
            border-collapse: collapse;
            //margin-top: 30px;
            text-align: center;
        }

        table, th, td {
            border: 1px solid #ddd;
        }

        th {
            background-color: rgb(126, 186, 0);
            color: white;
            padding: 10px;
        }

        td {
            padding: 8px;
        }

        .header-with-button {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .button-container {
            margin-top: 20px;  
        }

        button {
            padding: 12px 20px; 
            font-size: 12px; 
            border: none;
            border-radius: 8px;
            background-color: #4CAF50; 
            color: white;
            cursor: pointer;
        }

        @media screen and (max-width: 768px) {
            button {
                font-size: 10px; 
            }
        }

        @media screen and (max-width: 480px) {
            button {
                font-size: 8px;
            }
        }

        button:hover {
            background-color: #45a049; /* Slightly darker on hover */
        }

  
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/moment"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-moment"></script> 
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.16.9/xlsx.full.min.js"></script>
    <script>

        const dataAktywne = {{ data_aktywne }};
        const dataNieaktywne = {{ data_nieaktywne }};
        const dataNowosci = {{ data_nowosci }};
        const dataWszystko = {{ data_wszystko }};
        const dataKlasyfikacja = {{ klasyfikacja_data }};
        const dataStatusy = {{ statusy_data }};
        const dataZejscie = {{ zejscie_data }};
        const dataSuperkat = {{ superkat_data }};
        const dataRanking = {{ ranking_data }};

        let doughnutCharts = [];
        let lineCharts = [];
        let barCharts = [];

        const percentageLabelPlugin = {
            id: 'percentageLabel',
            afterDraw(chart) {
                const ctx = chart.ctx;
                const data = chart.data.datasets[0].data;
                const total = data.reduce((a, b) => a + b, 0);
                const availablePercentage = ((data[0] / total) * 100).toFixed(0);
                const centerX = chart.getDatasetMeta(0).data[0].x;
                const centerY = chart.getDatasetMeta(0).data[0].y;

                ctx.save();
                ctx.font = 'bold 42px Arial';
                ctx.fillStyle = 'grey';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(`${availablePercentage}%`, centerX, centerY);
                ctx.restore();
            }
        };

        function exportToExcel() {
            var data = {{ table_ava | tojson }};
            var rows = [];

            var headers = data.datasets.map(d => d.label);
            rows.push(headers);

            var numRows = data.datasets[0].data.length;
            for (var i = 0; i < numRows; i++) {
                var row = [];
                for (var j = 0; j < data.datasets.length; j++) {
                    row.push(data.datasets[j].data[i]);
                }
                rows.push(row);
            }

            var wb = XLSX.utils.book_new();
            var ws = XLSX.utils.aoa_to_sheet(rows);

            XLSX.utils.book_append_sheet(wb, ws, "Report Data");

            XLSX.writeFile(wb, "DostepnoscSI_report.xlsx");
            }
   
        function createCharts(data) {
            const labels = ['Dostępne', 'Niedostępne'];
            const chartIds = ['top100Chart', 'top500Chart', 'top1000Chart', 'top2000Chart', 'gt2000Chart', 'aclass', 'bclass', 'cclass', 'unclass'];
            chartIds.forEach((id, index) => {
                const ctx = document.getElementById(id).getContext('2d');
                if (doughnutCharts[index]) {
                    doughnutCharts[index].destroy(); 
                }
                doughnutCharts[index] = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: data[index],
                            backgroundColor: ['rgb(126, 186, 0)', '#cccccc']  
                        }]
                    },
                    options: {
                        plugins: {
                            legend: {
                                display: false
                            },
                            tooltip: {
                                enabled: true
                            }
                        }
                    },  
                    plugins: [percentageLabelPlugin]
                });
            });
        }

        function createLineChart(data) {
            const lineChartIds = ['klasChart', 'statusChart','zejscieChart'];  
            
            lineChartIds.forEach((id, index) => {
                const ctx = document.getElementById(id).getContext('2d');
                if (lineCharts[index]) {
                    lineCharts[index].destroy();
                }
                lineCharts[index] = new Chart(ctx, {
                    type: 'line',
                    data: data[index], 
                    options: {
                        scales: {
                            x: {
                                ticks: {
                                    autoSkip: false
                                }
                            },
                            y: {
                                ticks: {
                                    callback: function (value) {
                                        return (value * 100).toFixed(0) + '%';
                                    }
                                }
                            }
                        },
                                    plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function (tooltipItem) {
                                        const value = tooltipItem.raw;
                                        return (value * 100).toFixed(1) + '%';
                                    }
                                }
                            }
                        }
                    }
                });
            });
        }

        function createBarChart(data) {
            const BarChartIds = ['superkatChart', 'rankingChart'];
            
            BarChartIds.forEach((id, index) => {
                const ctx = document.getElementById(id).getContext('2d');
                if (barCharts[index]) {
                    barCharts[index].destroy();
                }
                barCharts[index] = new Chart(ctx, {
                    type: 'bar',
                    data: data[index],
                    options: {
                        scales: {
                            x: {
                                ticks: {
                                    autoSkip: false 
                                }
                            },
                            y: {
                                beginAtZero: false,
                                ticks: {
                                    callback: function (value) {
                                        return (value * 100).toFixed(0) + '%'; 
                                    }
                                }
                            }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function (tooltipItem) {
                                        const value = tooltipItem.raw;
                                        return (value * 100).toFixed(1) + '%'; 
                                    }
                                }
                            },
                            legend: {
                                display: false
                            }
                        }
                    },
                    plugins: [ 
                        {
                            id: 'percentageLabels', 
                            afterDatasetsDraw: function (chart) {
                                const ctx = chart.ctx;
                                chart.data.datasets.forEach(function (dataset, i) {
                                    const meta = chart.getDatasetMeta(i);
                                    meta.data.forEach(function (bar, index) {
                                        const data = dataset.data[index] * 100;
                                        ctx.fillStyle = '#fff'; 
                                        ctx.font = 'bold 12px Arial'; 
                                        ctx.textAlign = 'center'; 
                                        ctx.textBaseline = 'bottom'; 
                                        ctx.fillText(data.toFixed(0) + '%', bar.x, bar.y + 15); 
                                    });
                                });
                            }
                        }
                    ]
                });
            });
        }

        window.onload = function() {
            createCharts(dataWszystko);
            createLineChart([dataKlasyfikacja, dataStatusy, dataZejscie]);
            createBarChart([dataSuperkat,dataRanking]); 

            document.getElementById('btnAktywne').addEventListener('click', function() {
                createCharts(dataAktywne);
            });
            document.getElementById('btnNieaktywne').addEventListener('click', function() {
                createCharts(dataNieaktywne);
            });
            document.getElementById('btnNowosci').addEventListener('click', function() {
                createCharts(dataNowosci);
            });
            document.getElementById('btnWszystko').addEventListener('click', function() {
                createCharts(dataWszystko);
            });
        };
    </script>
</head>
<body>

    <header class="header">
        <div class="date">{{formatted_date}}</div>
        <h1>Raport Dostępności</h1>
        <img src="https://higrupa.pl/wp-content/uploads/2016/08/natura-drogerie-logo-biale-poprawne.png" alt="Logo">
    </header>

    <h2>Klasyfikacja według: Top 100 - Top >2000 - Klasyfikacji A/B/C</h2>

    <div class="buttons">
        <button id="btnAktywne">Aktywne</button>
        <button id="btnNieaktywne">Nieaktywne</button>
        <button id="btnNowosci">Nowości</button>
        <button id="btnWszystko">Wszystko</button>
    </div>

    <div class="charts">
        <div class="chart-container">
            <div class="chart-title">Top 100</div>
            <canvas id="top100Chart"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">Top 500</div>
            <canvas id="top500Chart"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">Top 1000</div>
            <canvas id="top1000Chart"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">Top 2000</div>
            <canvas id="top2000Chart"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">>Top 2000</div>
            <canvas id="gt2000Chart"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">A Klasyfikacja</div>
            <canvas id="aclass"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">B Klasyfikacja</div>
            <canvas id="bclass"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">C Klasyfikacja</div>
            <canvas id="cclass"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">Niesklasyfikowane</div>
            <canvas id="unclass"></canvas>
        </div>
        <div class="line-chart-container">
            <h2>Dostępność w czasie po klasyfikacji</h2>
            <canvas id="klasChart"></canvas>
        </div>
    
        <div class="line-chart-container">
            <h2>Dostępność w czasie po statusach</h2>
            <canvas id="statusChart"></canvas>
        </div>
    
        <div class="line-chart-container">
            <h2>Dostępność po wskaźniku zejścia w dniach</h2>
            <canvas id="zejscieChart"></canvas>
        </div>
    
        <div class="line-chart-container">
            <h2>Dostępność po superkategoriach</h2>
            <canvas id="superkatChart"></canvas>
        </div>

        <div class="line-chart-container">
            <h2>Dostępność po rankingu sprzedaży</h2>
            <canvas id="rankingChart"></canvas>
        </div>
    </div>

    <div class="header-with-button">
        <h2>Zestawienie SKU</h2>
        <div class="button-container">
            <button onclick="exportToExcel()">Eksport do Excel-a</button>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>DoZam</th>
                <th>Symkar</th>
                <th>Sprzedaz 30 dni</th>
                <th>Dostępność</th>
                <th>Schodzenie 1 szt. w dniach</th>
                <th>Ile dni niedostepny</th>
                <th>wskaźnik OOS</th>
            </tr>
        </thead>
        <tbody>
            {% for i in range(table_ava['labels']|length) %}
            <tr>
                <td>{{ table_ava['datasets'][0]['data'][i] }}</td>
                <td>{{ table_ava['datasets'][1]['data'][i] }}</td>
                <td>{{ table_ava['datasets'][2]['data'][i] }}</td>
                <td>{{ table_ava['datasets'][3]['data'][i] }}%</td>
                <td>{{ table_ava['datasets'][4]['data'][i] }}</td>
                <td>{{ table_ava['datasets'][5]['data'][i] }}</td>
                <td>{{ table_ava['datasets'][6]['data'][i] }}%</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""
