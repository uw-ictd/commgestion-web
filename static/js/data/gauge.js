function createGuageChart(backhaul_capacity_mbits) {
    // Render with an intial blank value. Will be updated asynchronously.
    // Use -1 instead of unknown so the needle will show up on initial load.
    let needleValue = [-1];

    let gauge_min = 0;
    let yellow_start = 0.8 * backhaul_capacity_mbits;
    let red_start = backhaul_capacity_mbits;
    let gauge_max = 1.2 * backhaul_capacity_mbits;

    // Follows the green, yellow, red bounds in each of the case
    let bounds = {
        'green': [gauge_min, yellow_start],
        'yellow': [yellow_start, red_start],
        'red': [red_start, gauge_max]
    };

    let units = "Mbps"
    let title = metricTitle + " " + units

    return Highcharts.chart('hc-gauge', {
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
                    linearGradient: {x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, '#FFF'],
                        [1, '#333']
                    ]
                },
                borderWidth: 0,
                outerRadius: '109%'
            }, {
                backgroundColor: {
                    linearGradient: {x1: 0, y1: 0, x2: 0, y2: 1},
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
                text: title
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
                valueDecimals: 3,
                valueSuffix: units,
            },
            wrap: false,
        }]

    });
}

function updateGaugeChart(chart, new_data) {
    chart.update({
        series: [{
            data: [new_data],
        }],
    });
}

$( document ).ready(function() {
    console.log("ready");
    let chart = createGuageChart(8)

    $.getJSON(api_endpoint).done((result) => {
        $("#warning-container").css("display", "none");
        let backhaul_total_bytes = result.backhaul.up_bytes_per_second + result.backhaul.down_bytes_per_second;
        let backhaul_total_mbits = (backhaul_total_bytes/1000000) * 8;
        backhaul_total_mbits = Number(backhaul_total_mbits.toFixed(3))
        updateGaugeChart(chart, backhaul_total_mbits);
    }).fail(() => {
        $("#warning-container").css("display", "inline");
        chart.update({
            title: {
                text: "",
            },
        });
    })
});
