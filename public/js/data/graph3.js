let seriesData = generateData();

function graph(d) {
    Highcharts.chart('graph-3', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Browser market shares in January, 2018'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
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
        series: [{
                name: 'Brands',
                colorByPoint: true,
                   data: d}
                ]});

}

function generateData() {
    let array = [];
    for (let i = 0; i < 10; i++) {
        let local_name = "str " + i;
        let local_value = 100;
        array.push({name: local_name, value: local_value});
    }
    graph(array);
}