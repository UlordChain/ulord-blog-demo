
Project Profile [中文版](https://github.com/UlordChain/ulord-blog-demo/blob/master/js/READEME_ZH.MD)
------
A blog system demo of ulord open platform based on nodejs middle layer, express framework and paython background.</br>

Effect
------
The main part is divided into the front desk including the user registration login panel, the article content list, and the pagination; the content details page including the article content display, the article payment view, and the article release page,etc.</br>

Operating environment:
------
In node.js v8 version of Windows, express v4.13.1 is running properly.</br>

Installation
------
    git clone git@github.com:UlordChain/ulord-blog-demo.git
    cd /js/ulord-blog  
    npm install  
    npm start

Attention: 
------
Distributed storage needs ipfs technology. Check ipfs-api for detailed documentation on[https://github.com/ipfs/js-ipfs-api](https://github.com/ipfs/js-ipfs-api)。</br>

#### Introduce CDN
    <script src="https://unpkg.com/ipfs-api/dist/index.js"></script>
    
#### The CDN-based IPFS API provides the IpfsApi constructor as a method of the global window object. as follows:

    var ipfs = window.IpfsApi('localhost', '5001')   //Build server locally
    
    var ipfs = window.IpfsApi('114.67.37.2', '20418')   //Build server Externally

#### Whether the local test is successfully built
    ipfs.id()
    .then((id) => {
      console.log('my id is: ', id)
    })
    .catch((err) => {
      console.log('Fail: ', err)
    })
   
#### Call ipfs-api
    ipfs.files.get(data,function (err,files) {
      if (err || typeof files == "undefined") {
        console.log(err);
      } else {
        console.log(files);
      }
    })
