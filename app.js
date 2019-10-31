var express = require('express');
var nunjucks = require('nunjucks');
var app = express();

//js/data contains the static gauge javascript files
//css folder contains files
app.use(express.static('js/data/'));
app.use(express.static('css'));

var PATH_TO_TEMPLATES = '.' ;
nunjucks.configure(PATH_TO_TEMPLATES, {
    autoescape: true,
    express: app
});

app.get('/home.html', function(req, res) {
    return res.render('index.html') ;
});

app.set('views', './views'); //directory where template files will be located

app.set('view engine', 'pug'); //using Pug type template engine

app.get('/', function (req, res) { //route to index.pug file
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})

module.exports = app;