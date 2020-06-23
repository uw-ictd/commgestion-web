function createGuageChart(chartType) {
    let needleValue = dataFromServer;
    let guageParameterString = metricTitle;
    // Follows the green, yellow, red bounds in each of the case
    let bounds = {
        'green': [0, 400],
        'yellow': [400, 600],
        'red': [600, 1000]
    };
    if (chartType === 'Mbps') {
        newValueInMbps = dataFromServer[0] * 0.008;
        needleValue = [newValueInMbps];
        bounds = {
            'green': [0, 6.4],
            'yellow': [6.4, 11.2],
            'red': [11.2, 16]
        };
        guageParameterString = guageParameterString.replace('KBps', 'Mbps');
    } else if (chartType === 'MBps') {
        newValueInMBps = dataFromServer[0] * 0.001;
        needleValue = [newValueInMBps];
        bounds = {
            'green': [0, 0.8],
            'yellow': [0.8, 1.4],
            'red': [1.4, 2.0]
        };
        guageParameterString = guageParameterString.replace('KBps', 'MBps');
    }
    Highcharts.chart('hc-gauge', {
        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: gaugeGraphTitle
        },
        credits: {
            enabled: false
        },
        pane: {
            startAngle: -150,
            endAngle: 150,
            background: [{
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                    ]
                },
                borderWidth: 0,
                outerRadius: '109%'
            }, {
                backgroundColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0, '#333'],
                        [1, '#FFF']
                    ]
                },
                borderWidth: 1,
                outerRadius: '107%'
            }, {
                // default background
            }, {
                backgroundColor: '#DDD',
                borderWidth: 0,
                outerRadius: '105%',
                innerRadius: '103%'
            }]
        },

        // the value axis
        yAxis: {
            min: bounds['green'][0],
            max: bounds['red'][1],

            minorTickInterval: 'auto',
            minorTickWidth: 1,
            minorTickLength: 10,
            minorTickPosition: 'inside',
            minorTickColor: '#666',

            tickPixelInterval: 30,
            tickWidth: 2,
            tickPosition: 'inside',
            tickLength: 10,
            tickColor: '#666',
            labels: {
                step: 2,
                rotation: 'auto'
            },
            title: {
                text: guageParameterString
            },
            plotBands: [{
                from: bounds['green'][0],
                to: bounds['green'][1],
                color: '#55BF3B' // green
            }, {
                from: bounds['yellow'][0],
                to: bounds['yellow'][1],
                color: '#DDDF0D' // yellow
            }, {
                from: bounds['red'][0],
                to: bounds['red'][1],
                color: '#DF5353' // red
            }]
        },

        series: [{
            name: 'Current network use',
            data: needleValue,
            tooltip: {
                valueSuffix: chartType
            }
        }]

    });
}

$("#guageDataType").change(function() {
    chartType = $("#guageDataType option:selected").val();
    console.log(chartType);
    createGuageChart(chartType)
});

$( document ).ready(function() {
    $.getJSON(api_endpoint, result => {
        console.log("Received query result")
        console.log(result)
        let backhaul_total_bytes = result.backhaul.up_bytes_per_second + result.backhaul.down_bytes_per_second;
        let ran_total_bytes = result.ran.up_bytes_per_second + result.ran.down_bytes_per_second;
        let backhaul_total_kbytes = backhaul_total_bytes/1000;
        dataFromServer = [backhaul_total_kbytes];
        console.log(backhaul_total_bytes)
        createGuageChart("KBps")
    })
});
