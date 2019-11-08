// Build the chart
Highcharts.chart('graph-5', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Uso de datos comunitarios'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: false
            },
            showInLegend: true
        }
    },
    series: [{
        name: 'Usuarios',
        colorByPoint: true,
        data: [{
            name: 'Usuario 1',
            y: 61.41,
        }, {
            name: 'Usuario 2',
            y: 11.84
        }, {
            name: 'Usuario 3',
            y: 10.85
        }, {
            name: 'Usuario 4',
            y: 4.67
        }, {
            name: 'Usuario 5',
            y: 4.18
        }, {
            name: 'Other',
            y: 7.05
        }]
    }]
});