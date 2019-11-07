Highcharts.chart('user-data', {

    title: {
        text: 'User Consumption vs Community Average'
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        data: [ 
            [Date.UTC(2019, 8, 1, 6, 20), 29.9],
            [Date.UTC(2019, 8, 1, 6, 21), 71.5],
            [Date.UTC(2019, 8, 1, 6, 22), 106.4],
            [Date.UTC(2019, 8, 1, 6, 23), 29.9],
            [Date.UTC(2019, 8, 1, 6, 24), 71.5],
            [Date.UTC(2019, 8, 1, 6, 25), 106.4],
            [Date.UTC(2019, 8, 1, 6, 26), 29.9],
            [Date.UTC(2019, 8, 1, 6, 27), 71.5],
            [Date.UTC(2019, 8, 1, 6, 28), 106.4]
        ]
    }]
});