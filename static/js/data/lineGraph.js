//Some notes / reference:

//date object sytnax https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/UTC
//Date.UTC(year[, month[, day[, hour[, minute[, second[, millisecond]]]]]])
// months are 0 indexed, days are not.
function createLineChart(chartUnit, animate) {
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

    // Parse x axis to javascript date objects
    for (var i = 0; i < data.length; i++) {
        data[i] = [Date.parse(data[i][0]), data[i][1]];
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
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: false,
                },
                animation: animate
            }
        },
        series: [{
            data: data
        }]
    });
}

$("#thru-vs-time-unit").change(function() {
    chartUnit = $("#thru-vs-time-unit option:selected").val();
    createLineChart(chartUnit, true);
});

$( document ).ready(function() {
    chartUnit = $("#thru-vs-time-unit option:selected").val();
    createLineChart(chartUnit, false);
});
