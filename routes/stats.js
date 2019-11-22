let express = require('express');
let router = express.Router();
let constants = require('../constants');

/* GET stats page. */
router.get('/',
    function(req, res, next) {
        let rowBuilder = [
                ["thru-vs-time", "thru-by-app"],
                ["graph-3", "graph-4"]
        ];
        res.render(constants.STATISTICS_PAGE, {title: 'Express', user: req.user, rows: rowBuilder
        });
    });

module.exports = router;