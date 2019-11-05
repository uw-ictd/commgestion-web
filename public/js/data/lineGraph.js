//Some notes / reference:

//date object sytnax https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/UTC
//Date.UTC(year[, month[, day[, hour[, minute[, second[, millisecond]]]]]])
// months are 0 indexed, days are not. 

Highcharts.chart('thru-vs-time', {

    title: {
        text: 'Throughput v. Time'
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