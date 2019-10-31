var express = require('express');
var nunjucks = require('nunjucks');
var app = express();

var PATH_TO_TEMPLATES = '.' ;
nunjucks.configure(PATH_TO_TEMPLATES, {
    autoescape: true,
    express: app
});

app.get('/home.html', function(req, res) {
    return res.render('index.html') ;
});

//use static files from our project
app.use('*/js',express.static(path.join(__dirname, 'js/data/')));
app.use('*/css',express.static(path.join(__dirname, '/css')));


module.exports = app;