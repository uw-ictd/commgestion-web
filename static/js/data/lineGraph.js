//Some notes / reference:

//date object sytnax https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/UTC
//Date.UTC(year[, month[, day[, hour[, minute[, second[, millisecond]]]]]])
// months are 0 indexed, days are not.
function createLineChart(chartUnit) {
    let dataKBps = lookUpData("graph1");
    var data = [dataKBps.length];

    if(chartUnit === 'Mbps'){
        for (var i = 0; i < dataKBps.length; i++) {
            data[i] = [dataKBps[i][0], dataKBps[i][1]/1000];
        }
    }else if(chartUnit === 'MBps'){
        for (var i = 0; i < dataKBps.length; i++) {
            data[i] = [dataKBps[i][0], dataKBps[i][1]/1000/8];
        }
    }
    else{
        data = dataKBps;
    }

    let axisTitle = lookUpAxisLabel("graph2") + " (" + chartUnit + ")";
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
                "text": axisTitle
                    
            }
        },
        series: [{
            data: data
        }]
    });
}

$("#thru-vs-time-unit").change(function() {
    chartUnit = $("#thru-vs-time-unit option:selected").val();
    createLineChart(chartUnit);
});

$( document ).ready(function() {
    createLineChart('KBps');
});