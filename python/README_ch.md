# 优得

[English](https://github.com/UlordChain/ulord-blog-demo/tree/master/python)

一个轻量级的博客，将文章上传至ulord平台并进行定价，其他用户付费查看。所有交易信息均可通过ulord区块浏览器查阅

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
### 安装 python 和 pip
首先安装 python2.7.14 可以在[官网](https://www.python.org/)上下载

然后安装pip来管理你的python包

第三包使用pip来安装所需要的软件包
```bash
pip install -r requirements.txt
```
### 安装ipfs的go版客户端

go-ipfs是ipfs的go版客户端。通过它就可以连接到ipfs网络中。修改配置之后你就可以连接到ulord平台的ipfs平台中去。

你可以在[这里](https://github.com/ipfs/go-ipfs/releases/tag/v0.4.14)下载go-ipfs，根据你自己的系统环境去下载对应的版本。

需要在环境变量设置一下来使用ipfs。

##### windows

你可以使用 Tools/ipfs/install.bat 脚本安装ipfs。它是把ipfs.exe程序复制在你系统环境文件夹中
> 注意:默认你的系统换件文件夹是"C:\Windows\System32"。所有如果你的系统环境不在那里你应该手动修改脚本文件然后再执行。

#### linux

你可以使用 Tools/ipfs/install.bat 脚本安装ipfs。它是把ipfs.exe程序复制在你系统环境文件夹中
> 注意:默认你的系统换件文件夹是"/usr/local/bin/"。所有如果你的系统环境不包含那里你应该手动修改脚本文件然后再执行。


用下面的命令来初始化ipfs(Windows/Linux):
```bash
ipfs init
ipfs bootstrap rm --all
ipfs bootstrap add /ip4/114.67.37.2/tcp/20418/ipfs/QmctwnuHwE8QzH4yxuAPtM469BiCPK5WuT9KaTK3ArwUHu
ipfs config Datastore.StorageMax "1MB"
ipfs daemon
```
这是一个守护进程，别退出！

## 运行
```bash
python DBHelper\Manager.py

python server.py
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
