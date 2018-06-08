

const url = 'http://192.168.14.40:5000';

exports.login = function() {
  return url + '/user/login';
}

exports.getPublicKey = function() {
  return url + '/user/password';
}

exports.getBlogList = function() {
  return url + '/blog/all/list';
}

exports.register = function() {
  return url+'/user/regist';
}

exports.activity = function() {
  return url+'/user/activity';
}

exports.isbought = function() {
  return url+'/blog/isbought';
}

exports.publish = function() {
  return url + '/blog/publish';
}

exports.pay = function() {
  return url + '/pay/blogs';
}

exports.payAds = function() {
  return url + '/pay/ads';
}

exports.modify = function() {
  return url+'/user/modify';
}

exports.info = function() {
  return url+'/user/info';
}

exports.billings = function() {
  return url+'/user/billings';
}

exports.balance = function() {
  return url+'/user/balance';
}

exports.author = function() {
  return url+'/user/billings/income';
}

exports.customer = function() {
  return url+'/user/billings/outgo';
}

exports.published = function() {
  return url+'/user/published';
}

exports.bought = function() {
  return url+'/user/bought';
}

exports.delete = function() {
  return url+'/blog/delete'
}

exports.getDetails = function() {
  return url+'/blog/condition/id'
}

exports.update = function() {
  return url+'/blog/update'
}