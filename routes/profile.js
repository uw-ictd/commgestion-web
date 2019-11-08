let express = require('express');
let router = express.Router();
let constants = require('../constants');

/* GET profile page. */
router.get('/',
    function(req, res, next) {
        res.render(constants.USER_PROFILE, {title: 'Express', user: req.user});
    });

module.exports = router;
