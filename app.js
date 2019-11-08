let path = require('path');
let constants = require('./constants');
let express = require('express');
let nunjucks = require('nunjucks');
let app = express();

app.use(express.static(path.join(__dirname, 'public')));
nunjucks.configure(constants.PATH_TO_TEMPLATES, {
    autoescape: true,
    express: app
});

// Application logic

let indexRouter = require('./routes/index');
let statsRouter = require('./routes/stats');
let usersRouter = require('./routes/usuario');
let profileRouter = require('./routes/profile');
let publicRouter = require('./routes/public');

app.set('view engine', 'njk');

app.use('/', indexRouter);
app.use('/stats', statsRouter);
app.use('/usuario', usersRouter);
app.use('/profile', profileRouter);
app.use('/public', publicRouter);

module.exports = app; //exports as a module