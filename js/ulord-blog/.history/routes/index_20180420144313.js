var express = require('express');
var request = require('request');
var bodyParser = require('body-parser');
var router = express.Router();
var URL = require('url'); 

/* GET home page. */
router.get('/', function (req, res, next) {
  res.redirect('/login');
});

router.get('/login', function (req, res, next) {
  res.render('login', {
    code: ''
  });
});
router.post('/login', function (req, res) {
  var username = req.body.username;
  var userpass = req.body.password;
  var options = {
    url: 'http://192.168.14.240:5000/user/login',
    method: 'POST',
    json: true,
    headers: {
      "content-type": "application/json",
    },
    body: {
      username: username,
      password: userpass,
    }
  }
  console.log('请求开始');
  request(options, function (error, response, data) {
    console.log(data)
    if(data.errcode == '0'){
      // req.session.user = data;   
      console.log(data.result.token)
      res.cookie('token',data.result.token, { expires: new Date(Date.now() + 900000), httpOnly: true });
     
      res.render('login', {
        code: '1'
      })
      console.log(data);
    } else if (data.errcode == 6000) {
      res.json({
        "code": data.errcode
      })
    } 
  })

})
router.get('/register', function (req, res, next) {
  res.render('register', {
    code: ''
  });
});
router.post('/register', function (req, res) {
  var username = req.body.username;
  var userpass = req.body.password;
  var email = req.body.email;
  var phonenumber = req.body.phonenumber;
  
  var options = {
    url: 'http://192.168.14.240:5000/user/regist',
    method: 'POST',
    json: true,
    headers: {
      "content-type": "application/json",
    },
    body: {
      username: username,
      password: userpass,
      cellphone: phonenumber,
      email: email
    }
  }
  
  console.log('注册请求开始');
  request(options, function (error, response, data) {
    console.log(data, error);
    if(data.errcode == '0'){
      res.cookie('token',data.result.token, { expires: new Date(Date.now() + 900000), httpOnly: true });
      res.render('register', {
        code: '1'
      })
    } else if (data.msg == 'existing user') {
      res.render('register', {
        code: '-2'
      })
    } else if (data.msg == 'error cellphone') {
      res.render('register', {
        code: '-3'
      })
    } else if (data.msg == 'error email') {
      res.render('register', {
        code: '-4'
      })
    } else {
      res.render('register', {
        code: '-1'
      })
    }
  })
})

var jsonParse = bodyParser.json();
var urlencodedParser = bodyParser.urlencoded({extended: false})
router.get('/home', function (req, res, next) {
  console.log("ajax get列表请求开始")
  var url = URL.parse(req.url).query;
  var nav = URL.parse(req.url).pathname;
  console.log(url, nav);
  var page = 1;
  console.log(req.query.page);
  if(req.query.page){
    page = req.query.page;
  }
  var options = {
    url: 'http://192.168.14.240:5000/blog/all/list',
    method: 'POST',
    json: true,
    headers: {
      "content-type": "application/json",
      "token": req.cookies.token
    },
    body: {page: page}
  }
  console.log('get列表请求开始');
  request(options, function (error, response, data) {
    console.log(data);
    if(data.errcode == '0'){
      console.log(data.msg, data.result);
      if(url){
        url = url.replace(/\&page=[0-9]+/g, '');
      }
      var page_total =  Math.ceil(data.result.pages/10);//总页数
      var claimlist = [];
      data.result.data.forEach(function(item,index) {
        claimlist.push(item.claim_id);
      })

      var options2 = {
        url: 'http://192.168.14.240:5000/blog/isbought',
        method: 'POST',
        json: true,
        headers: {
          "content-type": "application/json",
          "token": req.cookies.token
        },
        body: {claim_ids: claimlist}
      }
      request(options2, function(error, response, data2) {
        var isPayList = [];
        if(data2.errcode == '0') {
         for(key in  data2.result) {
           isPayList.unshift(data2.result[key])
         }
         console.log('支付列表')
          console.log(isPayList);
          res.render('home', {
            page: page,
            data: data.result.data,
            error: '',
            total: page_total, 
            url:url,
            nav:nav.replace(/\//g, ''),
            isPayList: isPayList
          });

        }
      })


      
    
     
    
    } else {
      console.log(data);
    }
  })
});
// router.post('/home', urlencodedParser,  function (req, res, next) {
//   console.log('post列表请求开始');
//   console.log(req.body);
//   var options = {
//     url: 'http://192.168.14.40:5000/blog/all/list',
//     method: 'POST',
//     json: true,
//     contentType: json,
//     // body: {
      
//     // }
//   }
//   request(options, function (error, response, data) {
//     if(data.result == '1'){
//       res.render('data', data);
//       console.log(data.msg, data.result);
//     } else {
//       console.log(error);
//       console.log(data);
//     }
//   })
// })
router.get('/release', function (req, res, next) {
  res.render('release');
});

router.post('/release', urlencodedParser, function(req, res, next) {
  console.log(req.body);
  var options = {
    url: 'http://192.168.14.240:5000/blog/publish',
    method: 'POST',
    json: true,
    headers: {
      "content-type": "application/json",
      "token": req.cookies.token
    },
    body: {
      title: req.body.title,
      body: req.body.body,
      amount: req.body.amount,
      tag: req.body.tag,
      description: req.body.description
    }
  }

  console.log('发布请求开始');
  request(options, function (error, response, data) {
    console.log(data);
    if(data.errcode == '0'){
      res.json({
        code: 1
      });
    } else if (data.msg == "Insufficient amount"){
      res.json({
        code: -2
      });
    }
  })
})

router.post('/pay', urlencodedParser, function(req, res, next) {
  console.log(req.body);
  var options = {
    url: 'http://192.168.14.240:5000/pay',
    method: 'POST',
    json: true,
    headers: {
      "content-type": "application/json",
      "token": req.cookies.token
    },
    body: {
      password: req.body.password,
      title: req.body.title,
      auth: req.body.auth,
      amount: req.body.amount
    }
  }

  console.log('支付请求开始');
  request(options, function (error, response, data) {
    console.log(data);
    if(data.result == '1'){
      res.json({
        hash: data.msg,
        code: 1
      })
      console.log(data);
    } else if (data.msg == 'Insufficient amount') {
      res.json({
        code: -2
      })
    } else if (data.msg == 'error password') {
      res.json({
        code: -3
      })
    } 
  })
})

router.get('/details', function (req, res, next) {
  // var url = URL.parse(req.url).query;
  // var idValue = qs.parse(url)['id']
  res.render('details');
});
router.post('/details', urlencodedParser, function(req, res, next) {
  
  console.log(req.body.data)
  console.log(Utf8ArrayToStr(req.body.data));
  res.json('/details', {
    data: Utf8ArrayToStr(req.body.data)
  })
})

router.get('/info', function (req, res, neex) {
  // var options = {
  //   url: 'http://192.168.14.40:5000/user/info',
  //   method: 'GET',
  //   json: true,
  //   headers: {
  //     "token": req.cookies.token
  //   },
  // }
  // console.log('个人信息请求开始');
  // request(options, function (error, response, data) {
  //   console.log(data.msg);
  //   if (!error){
  //     res.render(
  //       'info', {
  //         data: data,
  //         error: error
  //       }
  //     )
  //   } else {
      
  //   }
    
  // })
  res.render('info');
});

router.get('/a', function(req, res, next) {
  res.render('a');
})
module.exports = router;