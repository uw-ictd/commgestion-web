let express = require('express');
let router = express.Router();
let constants = require('../constants');

/* GET home page. */
router.get('/',
    function(req, res, next) {
        res.render('_layout.njk', {title: 'Express', user: req.user});
    });

module.exports = router;
