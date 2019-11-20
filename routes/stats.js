let express = require('express');
let router = express.Router();
let constants = require('../constants');

/* GET stats page. */
router.get('/',
    function(req, res, next) {
        res.render(constants.STATISTICS_PAGE, {title: 'Express', user: req.user,
        rows: {
            top:["thru-vs-time", "thru-by-app"],
            bottom:["graph-3", "graph-4"]
        }
        });
    });

module.exports = router;
