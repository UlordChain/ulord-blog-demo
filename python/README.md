# Ulord-blog-demo

[中文](https://github.com/UlordChain/ulord-blog-demo/blob/master/python/README_ch.md)

Use ulord platform to create a single blog.

## Table of Contents
- [Instructions](#Instructions)
- [Features](#Features)
- [install](#install)
  - [install python and pip](#install-python-and-pip)
- [run](#run)
- [TODO](#todo)
- [API](#api)

## Instructions
This module is ulord-blog-demo's rear-end,completed by python2.7.It saves the title,price,description and other infos about blog into the Ulord block chain.The content of the blog will upload into the UDFS.The content of the blog which was saved into the Ulord block chain is a UDFS hash.Some queries will return it and then the font-ender can use it to show or download.

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
### install python and [py-ulord-api](https://github.com/UlordChain/py-ulord-api)
firstly you need to install python2.7.14 from the [website](https://www.python.org/downloads/release/python-2714/)

secondly clone [SDK program](https://github.com/UlordChain/py-ulord-api) and install.

```bash
git clone https://github.com/UlordChain/py-ulord-api.git
cd py-ulord-api
python setup.py install
```

## run
```bash
python junior.py
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


