项目简介
------
一个基于nodejs中间层、express框架及paython后台搭建的ulord博客demo。</br>

效果实现
------
主体分为前台包括用户注册登录面板，文章内容列表以及分页；内容详情页有文章内容展示，文章支付查看，文章的发布页等。</br>

运行环境:
------
在Windows下的node>8.0版本,express4.13.1版本运行正常。</br>

安装
------
    git clone git@github.com:UlordChain/ulord-blog-demo.git
    cd /js/ulord-blog  
    npm install  
    npm start

注意事项 
------
分布式存储引入需引用ipfs技术，ipfs文档移步[https://github.com/ipfs/js-ipfs-api](https://github.com/ipfs/js-ipfs-api)。</br>

#### 引入CDN
    <script src="https://unpkg.com/ipfs-api/dist/index.js"></script>
    
#### 基于CDN的IPFS API提供IpfsApi构造函数作为全局window对象的一种方法。例：
    var ipfs = window.IpfsApi('localhost', '5001')

#### 查看是否搭建成功
    ipfs.id()
    .then((id) => {
      console.log('my id is: ', id)
    })
    .catch((err) => {
      console.log('Fail: ', err)
    })
   
#### 调用ipfs接口
    ipfs.files.get(data,function (err,files) {
      if (err || typeof files == "undefined") {
        console.log(err);
      } else {
        console.log(files);
      }
    })
