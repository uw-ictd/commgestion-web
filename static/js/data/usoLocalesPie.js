Highcharts.chart('graph-3', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: lookUpTitle('graph3')
    },
    tooltip: {
        pointFormat: '{point.percentage:.1f}%'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [
        {
            colorByPoint: true,
            data: lookUpData("graph3")
        }
    ]
});