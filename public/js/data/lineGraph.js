//Some notes / reference:

//date object sytnax https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/UTC
//Date.UTC(year[, month[, day[, hour[, minute[, second[, millisecond]]]]]])
// months are 0 indexed, days are not. 
console.log(dataSet);
Highcharts.chart('thru-vs-time', {

    title: {
        text: 'Uso de datos en total de comunidad'
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        data: dataSet
    }]
});