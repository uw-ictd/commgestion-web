let express = require('express');
let router = express.Router();
let constants = require('../constants');
let um = require('../db/UserManager');

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
//    {
//        name: "Chrome",
//        y: 62.74,
//    },
//    {
//        name: "Firefox",
//        y: 10.57,
//    },
//    {
//        name: "Internet Explorer",
//        y: 7.23,
//    },
//    {
//        name: "Safari",
//        y: 5.58,
//    },
//    {
//        name: "Edge",
//        y: 4.02,
//    },
//    {
//        name: "Opera",
//        y: 1.92,
//    },
//    {
//        name: "Other",
//        y: 7.62,
//    }
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
                    // drilldown: "Locales"
                },
                {
                    name: "No Locales",
                    y: 38,
                    // drilldown: "No Locales"
                },
            ];

/* GET stats page. */
router.get('/',
    function(req, res, next) {
        let totalUsers = 0;
        um.graphTwoQuery().then(r=> {
            for (let i = 0; i < r.length; i++) {
                let temp = {
                    "name": r[i]["dataValues"]["name"],
                    "y": r[i]["dataValues"]["y"]
                }
                dataGraph2.push(temp);
                //finalArray.push(temp);
                //finalArray.push(JSON.parse(r[i]["dataValues"]));
            }
            console.log("final: " + dataGraph2);
        });
        um.findTotalUsers().then(r=> {
             totalUsers = r;
             let rowBuilder = [
                            ["thru-vs-time", "thru-by-app"],
                            ["graph-3", "graph-4"]
                    ];
                    let graphData = [dataGraph1, dataGraph2, dataGraph3, dataGraph4];
                    let data = JSON.stringify({
                                    "graph1": JSON.stringify(dataGraph1),
                                    "graph2": JSON.stringify(dataGraph2),
                                    "graph3": JSON.stringify(dataGraph3),
                                    "graph4": JSON.stringify(dataGraph4)
                                });
                    res.render(constants.STATISTICS_PAGE, {title: 'Express', user: req.user,
                        rows: rowBuilder, dataSets: data, totalUsers: totalUsers
                    });
        });
    });
module.exports = router;