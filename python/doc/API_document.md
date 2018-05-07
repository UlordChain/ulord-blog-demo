# API document

This is a document of blog web's API.It services for front-end.

## Table of Contents 目录 

- [Get Publickey 获取公钥](#get-publickey-获取公钥)
- [test encrypt 测试加密](#test-encrypt-测试加密)
- [Register 注册](#Register-注册)
- [Pay To User 优惠活动，给新注册的用户发10个ulord](#pay-to-user-优惠活动给新注册的用户发10个ulord)
- [Login 登录](#login----登录)
- [Install Go](#logout----登出)
- [Publish 发布博客](#publish--发布博客)
- [List All Blog 获取博客](#list-all-blog--获取博客)
- [check isbought 检查博客是否付费](#check-isbought--检查博客是否付费)
- [Pay blogs 支付博客](#pay-blogs-支付博客)
- [Pay ADs 支付广告](#pay-ads-支付广告)
- [List Personal Info 列出个人信息](#list-personal-info-列出个人信息)
- [List Personal Balance 列出个人余额](#list-personal-balance-列出个人余额)
- [List Personal Published 列出个人发布过的资源](#list-personal-published-列出个人发布过的资源)
- [List Personal Published num 列出个人发布过的资源数量](#list-personal-published-num-列出个人发布过的资源数量)
- [List Personal Bought 列出个人购买过的资源](#list-personal-bought-列出个人购买过的资源)
- [List Billings detail 列出个人账单详细信息(收入和支出接口总和)](#list-billings-detail-列出个人账单详细信息收入和支出接口总和)
- [List Billings 列出个人账单](#list-billings-列出个人账单)
- [List User's Outgos 列出个人支出](#list-users-outgos-列出个人支出)
- [List User's Incomes 列出个人收入账单](#list-users-incomes-列出个人收入账单)
- [Add Blog View 增加博客访问量](#add-blog-view-增加博客访问量)
- [Modify Personal Info 修改个人信息](#modify-personal-info-修改个人信息)
- [~~Modify Blog Info 修改文章信息~~](#modify-blog-info-修改文章信息)
- [~~Record Blog 添加博客访问~~](#record-blog-添加博客访问)
- [附录A:错误码对照表](#附录a错误码对照表)


## Get Publickey 获取公钥

URL:http://192.168.14.240:5000/user/password

method: get

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "pubkey": "..."
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

## test encrypt 测试加密

URL:http://192.168.14.240:5000/user/password

method: post

args:json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|password | 加密信息 |是|

```python
{
	"password":"加密后的密文"
}
```

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "password": "加密原文"
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

## Pay To User 优惠活动，给新注册的用户发10个ulord

URL:http://192.168.14.240:5000/user/activity

method: get

head:token

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "amount": "打的钱数"
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

## Logout    登出

URL:http://192.168.14.240:5000/user/logout

method: post，get

head:token

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": "success"
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
	"amount":0.02,
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
                "des": "这是使用UDFS和区块链生成的第2篇博客的描述信息",
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

## Pay blogs 支付博客

URL:http://192.168.14.240:5000/pay/blogs

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
        "udfs_hash":udfs_hash,
    }
}

# 支付成功返回文件的hash值，通过UDFS接口获取数据
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

## Pay ADs 支付广告

URL:http://192.168.14.240:5000/pay/ads

method:post

head:token

args：json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|author | 博客作者名 |是|
|claim_id | 博客id |是|

```python
{
	"author":"justin",
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
        "udfs_hash":udfs_hash,
    }
}

# 支付成功返回文件的hash值，通过UDFS接口获取数据
```

失败
```python
{
    "errcode": 错误码,
    "reason": "错误原因"
}
```

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
|category|查询条件|否

```python
{
    "page":1,
    "num":1,
    "category":0
}
```
> 默认为每页10条数据，返回第一页。查询条件为0-消费支出，1-广告收入，其他-所有

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "data": [
            {
                "claim_id": 资源的claim_id,
                "create_timed": 此条消费的时间,
                "customer": 消费者,
                "enabled": 资源是否删除,
                "id": 资源在DB中的id,
                "price": 0.6,  # 价格为正, 是发布者的收入
                "title": 资源标题,
                "txid": 此条消费的txid
            }
        ],
        "pages": 1,
        "total": 4
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

## List Personal Published num 列出个人发布过的资源数量

URL:http://192.168.14.240:5000/user/published/num

method: get

head:token

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "count": 0
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
|category|查询条件|否

```python
{
    "page":1,
    "num":1,
    "category":0            
}
```
> 默认为每页10条数据，返回第一页。查询条件为0-消费支出，1-广告收入，其他-所有

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "pages": 1,
        "records": [
            {
                "author": 资源发布者,
                "claim_id": 资源在链上的claim_id,
                "create_timed": 消费时间,
                "enabled": 资源是否删除,
                "id": 资源在DB中id,
                "price": 0.5, # 价格为正时, 是消费者的支出
                "title": 资源标题,
                "txid": 此条消费的txid
            }
        ],
        "total": 7
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

## List Billings detail 列出个人账单详细信息(收入和支出接口总和)

URL:http://192.168.14.240:5000/user/billings/details

method: post

head:token

args:json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|page|页数|否|
|num|每页显示数|否|

```python
{
    "page":1,
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
        "pages": 1,
        "records": [
            {  # 作为发布者, price正为资源收入
                "author": "uuu",
                "claim_id": "1eaeee8108d2ddeefebd5dc811c3722857e32165",
                "create_timed": "2018-04-21T08:40:07.045958+00:00",
                "customer": "935827234",
                "price": 0.65255,
                "title": "测试1111111",
                "txid": "346bb03f63287b8c19ff0deee42ffe561d266beaeea80cff58f8098c4a4f42ab"
            },
            {  # 作为发布者, price负为广告支出
                "author": "ttt",
                "claim_id": "ca067e452618915fab2d33cdb6cecca83ae95659",
                "create_timed": "2018-04-20T16:10:25.831104+00:00",
                "customer": "uuu",
                "price": -0.5,
                "title": "df",
                "txid": "d70c00b042b0fabd9279290f72af233d7e50f3092a0c341b05b3a7fc5cd784be"
            },
            {  #作为消费者, price正为资源支出
                "author": "tttttttttttt",
                "claim_id": "010d23be8ce1e23da9dad94c61618d1e0b484c77",
                "create_timed": "2018-04-20T16:09:38.522716+00:00",
                "customer": "uuu",
                "price": 0.02,
                "title": "the first blog",
                "txid": "1b05ff6234eb95f5836afe6e8caf2617206d1f0d540c3798d8a2004f1ac0e299"
            },
            {  # 作为消费者, price负为广告收入
                "author": "yyy",
                "claim_id": "798aedf4fab2fa77a77b56528abe6e50afce37e6",
                "create_timed": "2018-04-20T15:55:16.285238+00:00",
                "customer": "uuu",
                "price": -0.6,
                "title": "666",
                "txid": "851ecf55bd841322683a18a427fa69e6c6c49af8009c89ced6f0c1c12a620455"
            }
        ],
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

## List Billings 列出个人账单

URL:http://192.168.14.240:5000/user/billings/

method: get

head:token

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "customer_expenditure": {  # 消费支出
            "count": 2,  # 记录数量
            "sum": 1.17755  # 总支出
        },
        "customer_income": {  # 消费收入
            "count": 0,
            "sum": null
        },
        "publisher_expenditure": {  # 发布支出
            "count": 0,
            "sum": null
        },
        "publisher_income": {  # 发布收入
            "count": 0,
            "sum": null
        }
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

## ~~List Customer's Billings 列出作为消费者个人账单~~

## List User's Outgos 列出个人支出

~~URL:http://192.168.14.240:5000/user/billings/customer~~

URL:http://192.168.14.240:5000/user/billings/outgo

method: post

head:token

args:json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|page|页数|否|
|num|每页显示数|否|

```python
{
	"page":1,
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
        "pages": 1,
        "records": [
            {  # 用户作为发布者 支出广告费
                "author": "719355782",  # 发布者
                "claim_id": "870c3a35a8b82f1d4f8e89b89b5c7d3b80d6bc5b",
                "create_timed": "2018-04-21T08:39:25.883777+00:00",
                "customer": "935827234",  # 消费者
                "price": 0.525,  # 交易金额
                "title": "123123123123",
                "txid": "31af05db89decfcd561ba79fbd130aacb8f02de4b75e55f4548626c1d9732c51"
            },
            {  # 用户作为消费者, 支出资源消费
                "author": "tttttttttttt",
                "claim_id": "010d23be8ce1e23da9dad94c61618d1e0b484c77",
                "create_timed": "2018-04-21T11:55:43.680047+00:00",
                "customer": "719355782",
                "price": 0.02,
                "title": "the first blog",
                "txid": "f672a32a11c1eb82a7a1b17e93bc823132c7bc75c3ed990fd1e797c8a11fbe50"
            }
        ],
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

## ~~List Author's Billings 列出作为发布者个人账单~~

## List User's Incomes 列出个人收入账单

~~URL:http://192.168.14.240:5000/user/billings/author~~

URL:http://192.168.14.240:5000/user/billings/income

method: post

head:token

args:json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|page|页数|否|
|num|每页显示数|否|

```python
{
	"page":1,
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
        "pages": 1,
        "records": [
            {  # 用户作为消费这, 点击广告收入
                "author": "yyy",
                "claim_id": "798aedf4fab2fa77a77b56528abe6e50afce37e6",
                "create_timed": "2018-04-21T13:37:41.983595+00:00",
                "customer": "719355782",
                "price": 0.6,
                "title": "666",
                "txid": "d162db3c4185720d287b7fabbe560546c9bce06f0812fadeb9d78c8d0fe2a2aa"
            },
            {  # 用户作为发布者, 发布资源收入
                "author": "719355782",
                "claim_id": "870c3a35a8b82f1d4f8e89b89b5c7d3b80d6bc5b",
                "create_timed": "2018-04-21T09:47:05.902228+00:00",
                "customer": "zyding",
                "price": 0.525,
                "title": "123123123123",
                "txid": "b781f7c12aa7b7a43c22a5bea2ac56d6d15a1dbde7eeea9e2774f7e5f168df56"
            }
        ],
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

## Add Blog View 增加博客访问量

URL:http://192.168.14.240:5000/blog/views

method: post

head:token

args：json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|id | 数据库ID(不是claimID) |是|

```python
{
    'id':资源id
}
```

return:

成功
```python
{
    "errcode": 0,
    "reason": "success",
    "result": {
        "num": 修改影响行数
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

method: post

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
|~~title~~ | ~~标题 ~~ |~~是~~|
|~~body~~ | ~~博客内容 ~~ |~~否~~|
|~~amount~~ | ~~定价 ~~ |~~否~~|
|~~tag~~ | ~~标签 ~~ |~~否~~|
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
    60004:{'errcode':60001,'reason':'邮箱已存在.'},
    60005:{'errcode':60005,'reason':'数据库提交失败.'},
    60006:{'errcode':60006,'reason':'作者已失效.'},
    # 2. 请求参数验证相关
    60100:{'errcode':60100,'reason':'缺少参数.'},
    60101:{'errcode':60101,'reason':'参数长度不符.'},
    60102:{'errcode':60102,'reason':'参数必须为json格式.'},
    60103:{'errcode':60103,'reason':'需要token.'},
    60104:{'errcode':60104,'reason':'无效的token.'},
    60105:{'errcode':60105,'reason':'无效的邮箱.'},
    60106:{'errcode':60106,'reason':'无效的手机号.'},
    # 3.文件操作
    60200:{'errcode':60200,'reason':'上传文件失败.'},
    # 4.活动相关
    60300:{'errcode':60200,'reason':'活动取消.'},
    60301:{'errcode':60301,'reason':'已赠送.'},
}
```
