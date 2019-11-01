var path = require('path');
var express = require('express');
var nunjucks = require('nunjucks');
var app = express();

app.use(express.static(path.join(__dirname, 'public')));

var PATH_TO_TEMPLATES = './views' ;
nunjucks.configure(PATH_TO_TEMPLATES, {
    autoescape: true,
    express: app
});

//app.set('views', './views'); //directory where template files will be located

app.set('view engine', 'njk');

app.get('/', function (req, res) {
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


module.exports = app; //exports as a module