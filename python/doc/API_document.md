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

return:
```python
{
	"result": 1/0,
	"msg": "token/exception"
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

return:
```python
{
	"result": 1/0,
	"msg": "token/exception"
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

return:
```python
{
    "result": 1/0,
    "msg": "ClaimID/exception"
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

return:
> 暂定，可能会根据实际需求改动
```python
{
    "result": True/False,
	"msg": {
        	"list": [
                        {
                            "username":"test1"
                    		"timestamp": "1523276094",
                    		"tag ": ["tag1", "tag2"],
                    		"description": "this is a test",
                    		"title": "test1",
                    		"amount": "0"
                        }
                	   {
                            "username":"test2"
                            "timestamp": "1523276094",
                            "tag ": ["tag1", "tag2"],
                            "description": "this is a test",
                            "title": "test2",
                            "amount": "0"
                        }
                        ...
                ]
            "total":10
            }
        or exception
}

```

## Record Blog  添加博客访问

URL:http://192.168.14.240:5000/blog/record

method：post

head:token

args：json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|blog_ID|博客的ID|是|

return:
```python
{
	"result": 1/0,
	"msg": "None/exception"
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
|title | 标题 |是|
|auth | 作者 |是|
|amount | 价格 |是|


return:
```python
{
	"result": 1/0,
	"msg": "Hash/exception"
}
# 支付成功返回文件的hash值，通过IPFS接口获取数据
```

> IPFS 支持大部分语言的接口,[js参考链接](https://github.com/ipfs/js-ipfs-api)

## List Personal Info 列出个人信息

URL:http://192.168.14.240:5000/user/info

method: get

head:token

return:
```python
{
	"result": 1/0,
	"msg":  {
    	"username": "test",
    	"cellphone": "15538383838",
    	"Email": "998@163.com",
    	"balance": "16.8",
    	"publish_blogs": {
    		"blog1_title": {},
    		"blog2_title": {}
    	    },
    	"read_blogs": {
    		"blog1_title": {},
    		"blog2_title": {}
    	    },
    	"billing_details": {
    		"billing1_id": {},
    		"billing2_id": {}
    	    }
        }
        or exception
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

return:
```python
{
	"result": 1/0,
	"msg": "Success/Fail, try again."
}
```

## Modify Blog Info 修改文章信息

URL:http://192.168.14.240:5000/blog/modify

method: post

head:token

args：json

| arg      | comment   |  是否必填  |
| ----  | :-----:  |  :----:  |
|title | 标题 |是|
|body | 博客内容 |否|
|amount | 定价 |否|
|tag | 标签 |否|
|description|描述|否|

return:
```python
{
	"result": 1/0,
	"msg": "None/exception"
}
```


