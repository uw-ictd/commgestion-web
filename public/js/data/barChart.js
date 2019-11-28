// https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/demo/column-drilldown/
Highcharts.chart('thru-by-app', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Uso de datos en total de cada aplicacion'
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        title: {
            text: 'Rendimiento'
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
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b><br/>'
    },

    series: [
        {
            name: "Applications",
            colorByPoint: true,
            data: lookUpData("graph2")
        }
    ],
});