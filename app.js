var express = require( 'express' ) ;
var nunjucks = require( 'nunjucks' ) ;
var app = express() ;

var PATH_TO_TEMPLATES = '.' ;
nunjucks.configure( PATH_TO_TEMPLATES, {
    autoescape: true,
    express: app
} ) ;

app.get( '/home.html', function( req, res ) {
    return res.render( 'index.html' ) ;
} ) ;
app.listen( 3000 ) ;