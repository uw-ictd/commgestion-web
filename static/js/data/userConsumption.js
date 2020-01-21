console.log("hello");
Highcharts.chart('user-data', {

    title: {
        text: 'User Consumption vs Community Average'
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        data: dataSet
    }]
});