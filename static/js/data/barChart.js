// https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/demo/column-drilldown/
Highcharts.chart('thru-by-app', {
    chart: {
        type: 'column'
    },
    credits: {
        enabled: false
    },
    title: {
        text: lookUpTitle("graph2")
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        title: {
            text: lookUpAxisLabel("graph2")
        }

    },
    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,       
            }
        }
    },

    tooltip: {
        pointFormat: '{point.y:.2f}'
    },

    series: [
        {
            name: "Applications",
            colorByPoint: true,
            data: lookUpData("graph2")
        }
    ],
});