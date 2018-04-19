# API document

This is a document of blog web's API.It services for front-end.

## Register 注册

URL:http://192.168.14.240:5000/user/regist

method: post

args:json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|username | 用户名 |是|
|password | 密码 |是|
|cellphone | 手机号 |否|
|email | 邮箱 |否|

```python
{
	"username":"test",
	"password":"123",
	"cellphone":"15278559846"
	"email":"15574859643@163.com"
}
```

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "token": "adc23e30-42cc-11e8-a365-f48e388c65be"
    }
}
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

## Login    登录

URL:http://192.168.14.240:5000/user/login

method: post

args:json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|username | 用户名 |是|
|password | 密码 |是|

```python
{
	"username":"test",
	"password":"123"
}
```

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "token": "adc23e30-42cc-11e8-a365-f48e388c65be"
    }
}
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

## Publish  发布博客

URL:http://192.168.14.240:5000/blog/publish

method：post

head:token

args：json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|title | 标题 |是|
|body | 博客内容 |是|
|amount | 定价 |是|
|tag | 标签 |否|
|description|描述|否|

```python
{
	"title":"the first blog",
	"body":"This is a first blog.And it's just a test.",
	"amunt":0.02,
	"tag":["test","first"],
	"description":"This is a test blog."
}
```

return:

成功：
```python
{
    "errcode": 0,
    "reason": "success",
    "result":{
        "id":数据库id,
        "claim_id":资源在链上的id,
    }
}
```

失败：
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```
## List All Blog  获取博客

URL:http://192.168.14.240:5000/blog/all/list

method：post

head:token

args：json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|page|页数|否|
|num|每页显示数|否|

```python
{
	"page":1,
	"num":10
}
```
> 默认为每页10条数据，返回第一页

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        total:总条数,
        pages:总页数,
        data:
        [
            {
                "author": "justin",
                "claim_id": "45cdb43d78bd12ee3acfa9be7c56ae02d6c88d3e",
                "content_type": ".txt",
                "create_timed": "2018-04-12T15:47:34.446858+00:00",
                "currency": "ULD",
                "des": "这是使用IPFS和区块链生成的第2篇博客的描述信息",
                "id": 5,
                "price": 1.3,
                "status": 1,
                "tags": [
                    "C++",
                    "java",
                    "javascript",
                ],
                "title": "第2篇技术博客",
                "update_timed": null
            }
        ]
    }
}
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

## check isbought  检查博客是否付费

URL:http://192.168.14.240:5000/blog/isbought

method：post

head:token

args：json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|claim_ids|博客的id列表|是|

```python
{
	"claim_ids":[
        	"ec3c93680884d8b1aee25242f64f79f8bd847c57",
        	"a5b899fe01d633b6f0b809c4af2312524c081576",
        	"25e48b12694b4704aeff32ba0a568c21ad8dd5d6",
        	"e1b98bcc018950ac4684c663d0ea4fa9fc19543d",
        	"e1b98bcc018950ac4684c663d0ea4fa9fc19543f",
        	"2d4bbaf369464feeb90ac957af72a641f9a1bc9c"
    	]
}
```

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "25e48b12694b4704aeff32ba0a568c21ad8dd5d6": "QmUH2NbKrURA6hAmJnhfP4VTDtkjUs3fVCN2L7DoE3JLmm",
        "2d4bbaf369464feeb90ac957af72a641f9a1bc9c": false,  # 未付费
        "a5b899fe01d633b6f0b809c4af2312524c081576": "QmUH2NbKrURA6hAmJnhfP4VTDtkjUs3fVCN2L7DoE3JLmm",
        "e1b98bcc018950ac4684c663d0ea4fa9fc19543d": null,  # 没有此记录
        "e1b98bcc018950ac4684c663d0ea4fa9fc19543f": false,
        "ec3c93680884d8b1aee25242f64f79f8bd847c57": "QmUH2NbKrURA6hAmJnhfP4VTDtkjUs3fVCN2L7DoE3JLmm"
    }
}
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

## Pay 支付

URL:http://192.168.14.240:5000/pay

method:post

head:token

args：json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|password | 密码 |是|
|claim_id | 博客id |是|

```python
{
	"password":"123",
	"claim_id":"ec3c93680884d8b1aee25242f64f79f8bd847c57"
}
```

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result":{
        "ipfs_hash":ipfs_hash,
    }
}

# 支付成功返回文件的hash值，通过IPFS接口获取数据
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```
> IPFS 支持大部分语言的接口,[js参考链接](https://github.com/ipfs/js-ipfs-api)

## List Personal Info 列出个人信息

URL:http://192.168.14.240:5000/user/info

method: get

head:token

return:

成功
```python
{
	'errcode':0,
        'reason':'success',
        'result':{
    	    "username": "test",
            "cellphone":"15278559846",
			"email":"15574859643@163.com"
            }
}
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

## List Personal Balance 列出个人余额

URL:http://192.168.14.240:5000/user/balance

method: get

head:token

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result":{
        "total":总余额,
        "confirmed":已确认余额,
        "unconfirmed":未确认余额,
        "unmatured":未成熟的余额(挖矿所得,100个块才成熟),
    }
}
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

## List Personal Published 列出个人发布过的资源

URL:http://192.168.14.240:5000/user/published

method: post

head:token

args:json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|page|页数|否|
|num|每页显示数|否|

```python
{
	"page":2,
	"num":2
}
```
> 默认为每页10条数据，返回第一页

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "data": [
            {
                "author": "shu",
                "claim_id": "b7fb27065dd919968c9d4188a4bdbff1e3d1a668",
                "content_type": ".txt",
                "create_timed": "2018-04-17T09:25:27.427384+00:00",
                "currency": "ULD",
                "des": "shu的第一篇博客",
                "id": 23,
                "price": 1,
                "status": 1,
                "tags": [
                    "go",
                    "python",
                    "ruby"
                ],
                "title": "shu的第一篇博客",
                "update_timed": null
            }
        ],
        "pages": 2,
        "total": 2
    }
}
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

## List Personal Bought 列出个人购买过的资源

URL:http://192.168.14.240:5000/user/bought

method: post

head:token

args:json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|page|页数|否|
|num|每页显示数|否|

```python
{
	"page":6,
	"num":6
}
```
> 默认为每页10条数据，返回第一页

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "data": [
            {
                "author": "user2",
                "claim_id": "c51fe46a429aa4d76b800cd17e771392d1af90b8",
                "content_type": ".txt",
                "create_timed": "2018-04-16T09:06:56.477060+00:00",
                "currency": "ULD",
                "des": "blog description",
                "id": 13,
                "price": 0.5,
                "status": 1,
                "tags": [
                    "Ruby",
                    "Python"
                ],
                "title": "first blog12",
                "update_timed": null
            }
        ],
        "pages": 6,
        "total": 6
    }
}
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

## Modify Personal Info 修改个人信息
URL:http://192.168.14.240:5000/user/modify

method: get

head:token

args：json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|username | 用户名 |否|
|password | 原始密码 |是|
|cellphone | 手机号 |否|
|email | 邮箱 |否|
|new_password | 新密码 |否|

```python
{
	"username":"test1",
	"password":"123",
	"cellphone":"15574257777",
	"email":"7778547888@163.com",
	"new_password":"111"
}
```

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result":{
        "userid":5,
        "username":"test1",
        "email":"7778547888@163.com",
        "cellphone":"15574257777"
    }
}
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

## ~~Modify Blog Info 修改文章信息~~

~~URL:http://192.168.14.240:5000/blog/modify~~

~~method: post~~

~~head:token~~

~~args：json~~

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|~~title~~ | ~~标题 ~~|~~是~~|
|~~body~~ | ~~博客内容 ~~|~~否~~|
|~~amount~~ | ~~定价 ~~|~~否~~|
|~~tag~~ | ~~标签 ~~|~~否~~|
|~~description~~|~~描述~~|~~否~~|

~~return:~~
```python
{
	"result": 1/0,
	"msg": "None/exception"
}
```

## ~~Record Blog 添加博客访问~~

~~URL:http://192.168.14.240:5000/blog/record~~

~~method：post~~

~~head:token~~

~~args：json~~

| arg     | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|~~blog_ID~~ | ~~博客的ID~~ |~~是~~|

~~return:~~
```python
{
	"result": 1/0,
	"msg": "None/exception"
}
```

## 附录A:错误码对照表

```python
{
    # 正常
    0:{'errcode':0,'reason':'success'},  # 可以重写reason与result内容

    # HTTP协议错误码
    400:{'errcode':400,'reason':'错误的请求.'},
    403:{'errcode':403,'reason':'您没有权限进行此操作.'},
    404:{'errcode':404,'reason':'Api不存在.'},
    405:{'errcode':405,'reason':'http请求方法不允许.'},
    500:{'errcode':500,'reason':'Api出错了, 请检查url以及参数.'},

    # 系统级错误码
    10001:{'errcode':10001,'reason':'错误的请求KEY.'},
    10002:{'errcode':10002,'reason':'该KEY无请求权限.'},
    10003:{'errcode':10003,'reason':'KEY过期.'},
    10004:{'errcode':10004,'reason':'被禁止的IP.'},
    10005:{'errcode':10005,'reason':'被禁止的KEY.'},
    10006:{'errcode':10006,'reason':'当前IP请求超过限制.'},
    10007:{'errcode':10007,'reason':'请求超过次数限制.'},
    10008:{'errcode':10008,'reason':'系统内部异常.'},
    10009:{'errcode':10009,'reason':'接口维护.'},
    10010:{'errcode':10010,'reason':'接口停用.'},
    10011:{'errcode':10011,'reason':'当前没有登录用户,请登录.'},
    10012:{'errcode':10012,'reason':'缺少应用KEY值.'},
    10013:{'errcode':10013,'reason':'无权限进行此操作.'},

    # 服务级错误码
    # 1. DB查询验证
    20000:{'errcode':20000,'reason':'用户已存在.'},
    20001:{'errcode':20001,'reason':'邮箱已存在.'},
    20002:{'errcode':20002,'reason':'应用名已存在.'},
    20003:{'errcode':20003,'reason':'用户不存在.'},
    20004:{'errcode':20004,'reason':'密码错误.'},
    20005:{'errcode':20005,'reason':'数据不存在.'},
    20006:{'errcode':20006,'reason':'用户被禁用.'},
    20007:{'errcode':20007,'reason':'资源不存在.'},
    20008:{'errcode':20008,'reason':'资源需付费.'},

    # 2. 请求参数验证相关
    20100:{'errcode':20100,'reason':'缺少参数.'},
    20101:{'errcode':20101,'reason':'参数长度不符.'},
    20102:{'errcode':20102,'reason':'参数必须为json格式.'},
    # 3. 钱包相关接口调用
    20200:{'errcode':20200,'reason':'调用钱包接口失败.'},
    20201:{'errcode':20201,'reason':'资源发布失败.'},
    20202:{'errcode':20202,'reason':'资源消费失败.'},
    20203:{'errcode':20203,'reason':'查询余额失败.'},
    20204:{'errcode':20204,'reason':'创建钱包失败.'},

    # 应用服务级错误码
    # 1、DB查询验证
    60000:{'errcode':60000,'reason':'用户已存在.'},
    60001:{'errcode':60001,'reason':'邮箱已存在.'},
    60002:{'errcode':60002,'reason':'用户不存在.'},
    60003:{'errcode':60003,'reason':'密码错误.'},
    60004:{'errcode':60001,'reason':'邮箱已存在.'}
    60005:{'errcode':60005,'reason':'数据库提交失败.'}    
    # 2. 请求参数验证相关
    60100:{'errcode':60100,'reason':'缺少参数.'},
    60101:{'errcode':60101,'reason':'参数长度不符.'},
    60102:{'errcode':60102,'reason':'参数必须为json格式.'},
    60103:{'errcode':60103,'reason':'需要token.'},
    60104:{'errcode':60104,'reason':'无效的token.'},
    60105:{'errcode':60105,'reason':'无效的邮箱.'},
    60106:{'errcode':60106,'reason':'无效的手机号.'},    
    # 3.其他操作    	
    60200:{'errcode':60200,'reason':'上传文件失败.'},
}
```
