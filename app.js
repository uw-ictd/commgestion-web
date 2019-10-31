var express = require('express');
var nunjucks = require('nunjucks');
var app = express();

//js/data contains the static gauge javascript files
//css folder contains files
app.use(express.static('js/data/'));
app.use(express.static('css'));

var PATH_TO_TEMPLATES = './views' ;
nunjucks.configure(PATH_TO_TEMPLATES, {
    autoescape: true,
    express: app
});

app.get('/home.html', function(req, res) {
    return res.render('index.html') ;
});

//app.set('views', './views'); //directory where template files will be located

//app.set('view engine', 'pug'); //using Pug type template engine
app.set('view engine', 'njk');

app.get('/', function (req, res) { //route to index.pug file
  return res.render('_layout.njk');
})
app.get('/stats', function(req, res) {
    return res.render('stats.njk');
})

app.get('/usuario', function(req, res){
    return res.render('usuario.njk');
})

app.get('/profile', function(req, res){
    return res.render('profile.njk')
})

app.get('/public', function(req, res){
    return res.render('public_info.njk')
})


module.exports = app;