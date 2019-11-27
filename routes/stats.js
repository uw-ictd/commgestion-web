let express = require('express');
let router = express.Router();
let constants = require('../constants');

let dataGraph1 = [ 
            [Date.UTC(2019, 8, 1, 6, 20), 29.9],
            [Date.UTC(2019, 8, 1, 6, 21), 71.5],
            [Date.UTC(2019, 8, 1, 6, 22), 106.4],
            [Date.UTC(2019, 8, 1, 6, 23), 29.9],
            [Date.UTC(2019, 8, 1, 6, 24), 71.5],
            [Date.UTC(2019, 8, 1, 6, 25), 106.4],
            [Date.UTC(2019, 8, 1, 6, 26), 29.9],
            [Date.UTC(2019, 8, 1, 6, 27), 71.5],
            [Date.UTC(2019, 8, 1, 6, 28), 106.4]
        ];
let dataGraph2 = [
                {
                    name: "Chrome",
                    y: 62.74,
                },
                {
                    name: "Firefox",
                    y: 10.57,
                },
                {
                    name: "Internet Explorer",
                    y: 7.23,
                },
                {
                    name: "Safari",
                    y: 5.58,
                },
                {
                    name: "Edge",
                    y: 4.02,
                },
                {
                    name: "Opera",
                    y: 1.92,
                },
                {
                    name: "Other",
                    y: 7.62,
                }
            ];
let dataGraph3 = [
                {
                    name: "Locales",
                    y: 62,
                },
                {
                    name: "Extranjeros",
                    y: 38,
                },
            ];
let dataGraph4 = [
                {
                    name: "Locales",
                    y: 62,
                    drilldown: "Locales"
                },
                {
                    name: "No Locales",
                    y: 38,
                    drilldown: "No Locales"
                },
            ];

/* GET stats page. */
router.get('/',
    function(req, res, next) {
        let rowBuilder = [
                ["thru-vs-time", "thru-by-app"],
                ["graph-3", "graph-4"]
        ];
        let data = [
                [dataGraph1, dataGraph2],
                [dataGraph3, dataGraph4]
        ];
        res.render(constants.STATISTICS_PAGE, {title: 'Express', user: req.user, rows: rowBuilder, dataSets: data
        });
    });

module.exports = router;