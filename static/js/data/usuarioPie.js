// Build the chart
Highcharts.chart('graph-5', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    credits: {
        enabled: false
    },
    accessibility: {
        announceNewData: {
            enabled: true
        },
        point: {
            valueSuffix: '%'
        }
    },
    title: {
        text: usagePieTitle,
    },
    tooltip: {
        pointFormat: '<b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '{point.name}: {point.percentage:.1f}%'
            },
            // showInLegend: true
        }
    },
    series: [{
        data: dataFromServer
    }],
    drilldown: {
        series: [
            drillDownInfo
        ]
    },
    lang: {
        noData: noDataErrorMessage,
        useHTML: true
    }
});