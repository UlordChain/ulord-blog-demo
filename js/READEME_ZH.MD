项目简介
------
一个基于nodejs中间层、express框架及paython后台搭建的ulord博客系统demo。</br>

效果实现
------
主体分为前台包括用户注册登录面板，文章内容列表以及分页；内容详情页有文章内容展示，文章支付查看，文章的发布页等。</br>

运行环境:
------
在Windows环境下的node.js v8版本,express v4.13.1版本运行正常。</br>

安装
------
    git clone git@github.com:UlordChain/ulord-blog-demo.git
    cd /js/ulord-blog  
    npm install  
    npm start

注意事项 
------
分布式存储需引用ipfs技术，查看ipfs-api详细文档移步[https://github.com/ipfs/js-ipfs-api](https://github.com/ipfs/js-ipfs-api)。</br>

#### 引入CDN
    <script src="https://unpkg.com/ipfs-api/dist/index.js"></script>
    
#### 基于CDN的IPFS API提供IpfsApi构造函数作为全局window对象的一种方法。如下：

    var ipfs = window.IpfsApi('localhost', '5001')   //本地搭建服务器
    
    var ipfs = window.IpfsApi('114.67.37.2', '20418')   //外部搭建服务器

#### 本地测试是否搭建成功
    ipfs.id()
    .then((id) => {
      console.log('my id is: ', id)
    })
    .catch((err) => {
      console.log('Fail: ', err)
    })
   
#### 调用ipfs-api接口
    ipfs.files.get(data,function (err,files) {
      if (err || typeof files == "undefined") {
        console.log(err);
      } else {
        console.log(files);
      }
    })
