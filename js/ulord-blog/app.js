var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var ejs = require('ejs');
var session = require('express-session')
var bodyParser = require('body-parser');


//引入路由文件
var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

//设置 application/json 大小限制
app.use(bodyParser.json({limit: '50mb'}));

//设置 application/x-www-form-urlencoded 大小限制
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.engine('html',ejs.__express);
app.set('view engine', 'html');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(cookieParser());

//设置session和cookie
app.use(session({
  secret: '12345',
  name: 'token1',
  cookie: {maxAge: 60000},
  resave: false,
  saveUninitialized: true,
}))

app.use('/', indexRouter);
app.use('/users', usersRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
