# Ulord

[中文](https://github.com/UlordChain/ulord-blog-demo/blob/master/python/README_ch.md)

Use ulord platform to create a single blog.

## Table of Contents
- [Features](#Features)
- [install](#install)
  - [install python and pip](#install-python-and-pip)
  - [install go-ipfs](#install-go-ipfs)
    - [windows](#windows)
    - [linux](#linux)
- [run](#run)
- [TODO](#todo)
- [API](#api)

## Features
> * resource pricing
> * every source infomation publishes on the ulord
> * every transaction can be queryed on the ulord
> * upload to the ulord's IPFS,don't worry about storage
> * windows environment
> * linux environment
> * mutil database,like sqlite,mysql,postgresql,eg.
> * easy config

## install
### install python and pip
firstly you need to install python2.7.14 from the [website](https://www.python.org/)

secondly install pip to manager your python packages

thirdly using pip to install packages
```bash
pip install -r requirements.txt
```
### install go-ipfs

go-ipfs is a tool of ipfs.You can connect the ipfs using it.Change the config and you can connect the ulord's IPFS.

You can download IPFS form [here](https://github.com/ipfs/go-ipfs/releases/tag/v0.4.14) and choose the right version for your environment.

And then you need set the environment variables including the ipfs.

#### Windows

You can use Tools/ipfs/install.bat to install ipfs.It will copy the ipfs.exe to your system environment.
> warnning:It will copy the file to "C:\Windows\System32".So if your system environment is not there you should modify the bat file handly and execute it.

#### Linux

You can use Tools/ipfs/install.sh to install ipfs.It will copy the ipfs.exe to your system environment.
> warnning:It will copy the file to "/usr/local/bin/".So if your system environment doesn't include there you should modify the bat file handly and execute it.

Then using the command to init your ipfs(Windows/Linux):
```bash
ipfs init
ipfs bootstrap rm --all
ipfs bootstrap add /ip4/114.67.37.2/tcp/20418/ipfs/QmctwnuHwE8QzH4yxuAPtM469BiCPK5WuT9KaTK3ArwUHu
ipfs config Datastore.StorageMax "1MB"
ipfs daemon
```
This is a daemon program.Don't exit!

## run
```bash
python dbHelper\dbManager.py

python server.py

```
## TODO
- [x] add TODO list
- [x] add login
- [x] add logout
- [x] add config
- [x] add encryption
- [x] add upload
- [x] linux environment
- [ ] add unit test
- [ ] docker environment

## API
This project serveres for the front end.API document is [here](https://github.com/UlordChain/ulord-blog-demo/blob/master/python/doc/API_document.md)


