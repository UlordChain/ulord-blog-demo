# 优得

[English](https://github.com/UlordChain/ulord-blog-demo/tree/master/python)

一个轻量级的博客，将文章上传至ulord平台并进行定价，其他用户付费查看。所有交易信息均可通过ulord区块浏览器查阅

## 目录
- [说明](#说明)
- [特性](#特性)
- [安装](#安装)
  - [安装 python 和 pip](#安装-python-和-ulord平台sdk)
- [运行](#运行)
- [计划清单](#计划清单)
- [接口](#接口)

## 说明
本目录为博客演示系统后台，由python2.7完成。将博客的标签、价格、描述等信息通过调用ulord平台API上传至ulord区块链中，内容则上传至UDFS中，保存在ulord平台中的内容为UDFS哈希值。查询返回UDFS哈希值。前端调用UDFS开发包去浏览或下载哈希值对应的内容。

## 特性

> * 资源定价
> * 所有资源都可在ulord平台上查阅
> * 所有交易均可在ulord平台查看
> * 文章上传至ulord平台上，服务端不必担心存储
> * windows 环境
> * linux 环境
> * 多类型数据库，支持sqlite、mysql、postgresql等
> * 配置简单

## 安装
### 安装 python 和 [ulord平台SDK](https://github.com/UlordChain/py-ulord-api)
首先安装 python2.7.14 可以在[官网](https://www.python.org/downloads/release/python-2714/)上下载

然后克隆[ulord平台SDK](https://github.com/UlordChain/py-ulord-api)项目并安装。

```bash
git clone https://github.com/UlordChain/py-ulord-api.git
cd py-ulord-api
python setup.py install
```

## 运行
```bash
python junior.py
```
## 计划清单
- [x] 添加计划清单
- [x] 添加登录
- [x] 添加登出
- [x] 添加配置文件
- [x] 添加加密
- [x] 添加上传
- [x] 适配linux环境
- [ ] 添加单元测试
- [ ] docker 环境

## 接口
这个项目只是为前端服务.接口文档看[这里](https://github.com/UlordChain/ulord-blog-demo/blob/master/python/doc/API_document.md)
