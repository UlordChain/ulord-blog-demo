var express = require('express');
var request = require('request');
var bodyParser = require('body-parser');
var router = express.Router();
var URL = require('url');

var api = require('./api.js');


/* GET home page. */
router.get('/', function(req, res, next) {
  res.redirect('/login');
});
/*--------------------获取公匙---------------------*/
router.post('/password', function(req, res, next) {
  var options = {
    url: api.getPublicKey(),
    method: 'GET',
    json: true,
    headers: {
      "content-type": "application/json"
    }
  }
  console.log(options);
  console.log('获取公匙')
  request(options, function(error, response, data) {
    console.log(data, error);
    res.json({
      code: data.errcode,
      publicKey: data.result.pubkey
    })
  })
})

/*---------------------登录------------------------*/

router.get('/login', function(req, res, next) {
  res.render('login', {
    code: ''
  });
});

router.post('/login', function(req, res) {
  var username = req.body.username;
  var userpass = req.body.password;
  var options = {
    url: api.login(),
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
  console.log('登录请求开始');
  request(options, function(error, response, data) {
    console.log(data)
    if (data.errcode == '0') {
      // req.session.user = data;   
      res.cookie('token', data.result.token, {
        expires: new Date(Date.now() + 86400000),
        httpOnly: true
      });
      res.json({
        code: data.errcode
      })
    } else {
      res.json({
        code: data.errcode
      })
    }
  })

})

/*---------------------注册------------------------*/

router.get('/register', function(req, res, next) {
  res.render('register', {
    code: ''
  });
});

router.post('/register', function(req, res) {
  var username = req.body.username;
  var userpass = req.body.password;
  var email = req.body.email;
  var phonenumber = req.body.phonenumber;
  var options = {
    url: api.register(),
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
  request(options, function(error, response, data) {
    console.log(data, error);
    if (data.errcode == '0') {
      res.cookie('token', data.result.token, {
        expires: new Date(Date.now() + 86400000),
        httpOnly: true
      });
      res.json({
        code: data.errcode,
        token: data.result.token
      })
    } else {
      res.json({
        code: data.errcode
      })
    }
  })
})

/*---------------------活动------------------------*/

router.post('/activity', function(req, res2, next) {
  console.log("活动请求开始")
  var options = {
    url: api.activity(),
    method: 'GET',
    json: true,
    headers: {
      "content-type": "application/json",
      "token": req.cookies.token
    },
  }
  request(options, function(error, response, data) {
    console.log('送币', data);
    if (data.errcode == '0') {
      console.log('成功')
      res2.json({
        code: data.errcode,
      })
    }
  })
})

/*---------------------获取home列表------------------------*/

var jsonParse = bodyParser.json();
var urlencodedParser = bodyParser.urlencoded({
  extended: false
})
router.get('/home', function(req, res, next) {
  console.log("ajax get列表请求开始")
  console.log(url);
  console.log('token', req.cookies.token);
  var url = URL.parse(req.url).query;
  var nav = URL.parse(req.url).pathname;
  console.log(url, nav);
  var page = 1;
  console.log(req.query.page);
  if (req.query.page) {
    page = req.query.page;
  }

  var options = {
    url: api.getBlogList(),
    method: 'POST',
    json: true,
    headers: {
      "content-type": "application/json",
      "token": req.cookies.token
    },
    body: {
      page: page
    }
  }

  console.log('get列表请求开始');
  request(options, function(error, response, data) {
    console.log(data)
    if (data.errcode == '0') {
      console.log('列表数据', data.result);
      if (url) {
        url = url.replace(/\&page=[0-9]+/g, '');
      }
      var page_total = Math.ceil(data.result.total / 10); //总页数
      var claimlist = [],
        isPayList = [];
      if (page_total !== 0) {
        data.result.records.forEach(function(item, index) {
          claimlist.push(item.claim_id);
        })
        console.log("claimlist", claimlist);
        var options2 = {
          url: api.isbought(),
          method: 'POST',
          json: true,
          headers: {
            "content-type": "application/json",
            "token": req.cookies.token
          },
          body: {
            claim_ids: claimlist
          }
        }

        request(options2, function(error, response, data2) {

          console.log('是否有哈希获取', data2)
          if (data2.errcode == '0') {
            for (key in data2.result) {
              isPayList.unshift(data2.result[key])
            }
            console.log(isPayList);
            res.render('home', {
              page: page,
              data: data.result.records,
              error: '',
              total: page_total,
              url: url,
              nav: nav.replace(/\//g, ''),
              data2: data2.result
            });

          }
        })
      } else {
        res.render('home', {
          page: page,
          data: data.result.records,
          error: '',
          total: page_total,
          url: url,
          nav: nav.replace(/\//g, ''),
          data2: {}
        });

      }

    } else {
      console.log('请求失败');
    }
  })
});
// router.post('/home', urlencodedParser,  function (req, res, next) {
//   console.log('post列表请求开始');
//   console.log(req.body);
//   var options = {
//     url: 'http://http://192.168.14.40:5000/blog/all/list',
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

/*--------------------发布------------------------*/

router.get('/release', function(req, res, next) {
  res.render('release');
});
router.post('/release', urlencodedParser, function(req, res, next) {
  console.log(req.body);
  var options = {
    url: api.publish(),
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
  request(options, function(error, response, data) {
    console.log(data);
    if (data.errcode == '0') {
      res.json({
        code: 1
      });
    } else if (data.msg == "Insufficient amount") {
      res.json({
        code: -2
      });
    }
  })
})

/*---------------------支付------------------------*/

router.post('/pay', urlencodedParser, function(req, res, next) {
  console.log(req.body);
  var options = {
    url: api.pay(),
    method: 'POST',
    json: true,
    headers: {
      "content-type": "application/json",
      "token": req.cookies.token
    },
    body: {
      password: req.body.password,
      claim_id: req.body.claim_id
    }
  }
  console.log('支付请求开始1');
  request(options, function(error, response, data) {
    console.log(data);
    if (data.errcode == '0') {
      res.json({
        hash: data.result.udfs_hash,
        code: data.errcode
      })
      console.log(data);
    } else {
      res.json({
        code: data.errcode
      })
    }
  })
})

/*---------------------广告------------------------*/

router.post('/ads', urlencodedParser, function(req, res, next) {
  console.log(req.body);
  var options = {
    url: api.payAds(),
    method: 'POST',
    json: true,
    headers: {
      "content-type": "application/json",
      "token": req.cookies.token
    },
    body: {
      author: req.body.author,
      claim_id: req.body.claim_id
    }
  }
  console.log('支付请求开始');
  request(options, function(error, response, data) {
    console.log(data);
    if (data.errcode == '0') {
      res.json({
        hash: data.result.udfs_hash,
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

/*---------------------文章详情------------------------*/

router.get('/details', function(req, res, next) {
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

/*---------------------修改个人信息----------------*/

router.post('/modify', function(req, res, next) {
  var username = req.body.username;
  var password = req.body.password;
  var email = req.body.email;
  var cellphone = req.body.cellphone;
  var new_password = req.body.new_password;
  console.log("修改个人信息开始")
  console.log(password, email, cellphone, new_password);
  console.log('原始密码', password)
  var options = {
    url: api.modify(),
    method: 'POST',
    json: true,
    headers: {
      "content-type": "application/json",
      "token": req.cookies.token
    },
    body: {
      password: password,
      email: email,
      cellphone: cellphone,
      new_password: new_password
    }
  }
  request(options, function(error, response, data) {
    console.log(data);
    res.json({
      code: data.errcode
    })
  })
})


/*---------------------广告------------------------*/

router.get('/info', function(req, res, neex) {
  var options = {
    url: api.info(),
    method: 'GET',
    json: true,
    headers: {
      "token": req.cookies.token
    },
  }
  console.log('个人信息请求开始', req.cookies.token);
  request(options, function(error, response, data) {
    console.log('个人信息', data);
    if (data.errcode == 0) {
        console.log('data7\<br\>')
        res.render('info',{
          code: data.errcode,
          data: data.result,
        })
      }
    })
  })
    
router.get('/balance', function(req, res, next) {
  var options = {
    url: api.balance(),
    method: 'get',
    json: true,
    headers: {
      "token": req.cookies.token,
    }
  }
  console.log("获取余额接口开始");
  request(options, function(error, response, data) {
    console.log("个人余额", data)
    if(data.errcode == 0) {
      res.json({
        "code": data.errcode,
        "data": data.result
      })
    }
  })
})

router.post('/billings', function(req, res, next) {
  var options = {
    url: api.billings(),
    method: 'post',
    json: true,
    headers: {
      "token": req.cookies.token,
    },
    body: {
      "sdate": req.body.sdate,
      "edate": req.body.edate
    }
  }
  console.log("获取账单总额接口开始");
  request(options, function(error, response, data) {
    console.log("账单总额", data)
    if(data.errcode == 0) {
      res.json({
        "code": data.errcode,
        "data": data.result
      })
    }
  })
})

router.post('/outgo', function(req, res, next) {
  var options = {
    url: api.customer(),
    method: 'post',
    json: true,
    headers: {
      "token": req.cookies.token,
    },
    body: {
      "sdate": req.body.sdate,
      "edate": req.body.edate,
      "page":  req.body.page,
    }
  }
  console.log("获取支出账单接口开始");
  request(options, function(error, response, data) {
    console.log("支出账单", data)
    if(data.errcode == 0) {
      res.json({
        "code": data.errcode,
        "data": data.result
      })
    }
  })
})

router.post('/income', function(req, res, next) {
  var options = {
    url: api.author(),
    method: 'post',
    json: true,
    headers: {
      "token": req.cookies.token,
    },
    body: {
      "sdate": req.body.sdate,
      "edate": req.body.edate,
      "page":  req.body.page,
    }
  }
  console.log("获取收入账单接口开始");
  request(options, function(error, response, data) {
    console.log("收入账单", data)
    if(data.errcode == 0) {
      res.json({
        "code": data.errcode,
        "data": data.result
      })
    }
  })
})

router.post('/published', function(req, res, next) {
  var options = {
    url: api.published(),
    method: 'post',
    json: true,
    headers: {
      "token": req.cookies.token,
    },
    body: {
      "sdate": req.body.sdate,
      "edate": req.body.edate,
      "page":  req.body.page,
    }
  }
  console.log("已发布资源");
  request(options, function(error, response, data) {
    console.log("已发布资源", data)
    if(data.errcode == 0) {
      res.json({
        "code": data.errcode,
        "data": data.result
      })
    }
  })
})

router.post('/delete', function(req, res, next) {
  var options = {
    url: api.delete(),
    method: 'post',
    json: true,
    headers: {
      "token": req.cookies.token,
    },
    body: {
      "id": req.body.id,
      "password": req.body.password,
    }
  }
  console.log("删除资源");
  request(options, function(error, response, data) {
    console.log("删除资源", data)
    if(data.errcode == 0) {
      res.json({
        "code": data.errcode,
        "data": data.result
      })
    }
  })
})

router.post('/getDetails', function(req, res, next) {
  console.log(req.body.id);
  var options = {
    url: api.getDetails(),
    method: 'post',
    json: true,
    headers: {
      "token": req.cookies.token,
    },
    body: {
      "ids": [req.body.id]
    }
  }
  console.log("获取文章详情");
  request(options, function(error, response, data) {
    console.log("获取文章详情", data)
    if(data.errcode == 0) {
      res.json({
        "code": data.errcode,
        "data": data.result
      })
    }
  })
})

router.post('/isbought', function(req, res, next) {
var options = {
  url: api.isbought(),
  method: 'POST',
  json: true,
  headers: {
    "content-type": "application/json",
    "token": req.cookies.token
  },
  body: {
    claim_ids: [req.body.id],
  }
}

request(options, function(error, response, data) {

  console.log('是否有哈希获取', data)
  if (data.errcode == '0') {
    res.json({
      code: data.errcode,
      data: data.result
    })
  }
})
})

router.post('/update', urlencodedParser, function(req, res, next) {
  console.log(req.body);
  var options = {
    url: api.update(),
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
      description: req.body.description,
      id: req.body.id,
      password: req.body.password
    }
  }

  console.log('修改文章请求开始');
  request(options, function(error, response, data) {
    console.log(data);
    if (data.errcode == '0') {
      res.json({
        code: 1
      });
    } else if (data.msg == "Insufficient amount") {
      res.json({
        code: -2
      });
    }
  })
})

router.get('/update', function(req, res, next) {
  res.render('update',{

  });
})
module.exports = router;