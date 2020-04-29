//Some notes / reference:

//date object sytnax https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/UTC
//Date.UTC(year[, month[, day[, hour[, minute[, second[, millisecond]]]]]])
// months are 0 indexed, days are not.
Highcharts.chart('thru-vs-time', {

    title: {
        text: lookUpTitle('graph1')
    },
    credits: {
        enabled: false
    },
    legend:{
        enabled: false
    },
    tooltip: {
        pointFormat: '{point.y:.2f}'
    },
    xAxis: {
        type: 'datetime'
    },
    "yAxis": {
        "title": {
            "text": 
                ('graph1')
        }
    },
    series: [{
        data: lookUpData("graph1")
    }]
});