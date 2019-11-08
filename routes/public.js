let express = require('express');
let router = express.Router();
let constants = require('../constants');

/* GET public page. */
router.get('/',
    function(req, res, next) {
        res.render(constants.PUBLIC_INFO, {title: 'Express', user: req.user});
    });

module.exports = router;
