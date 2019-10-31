var express = require('express');
var nunjucks = require('nunjucks');
var app = express();

//js/data contains the static gauge javascript files
//css folder contains files
app.use('*/js',express.static(path.join(__dirname, 'js/data/')));
app.use('*/css',express.static(path.join(__dirname, 'css')));
//could try these options too if doesn't work
//app.use(express.static('js/data/')); app.use(express.static('css));
//app.use('*/css',express.static('css'));

var PATH_TO_TEMPLATES = '.' ;
nunjucks.configure(PATH_TO_TEMPLATES, {
    autoescape: true,
    express: app
});

app.get('/home.html', function(req, res) {
    return res.render('index.html') ;
});

app.set('views', './views'); //directory where template files will be located

app.set('view engine', 'pug'); //use Pug template engine

module.exports = app;