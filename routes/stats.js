let express = require('express');
let router = express.Router();
let constants = require('../constants');

/* GET stats page. */
router.get('/',
    function(req, res, next) {
        res.render(constants.STATISTICS_PAGE, {title: 'Express', user: req.user});
    });

module.exports = router;
