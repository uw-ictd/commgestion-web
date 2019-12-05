let express = require('express');
let router = express.Router();
let constants = require('../constants');
let um = require('../db/UserManager');

/* GET user page. */
router.get('/',
    function(req, res, next) {
        res.render(constants.USERS_PAGE, {title: 'Express', user: req.user});
    });

module.exports = router;
