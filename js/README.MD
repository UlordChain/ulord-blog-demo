  
本地测试
安装node环境，
安装mongodb数据库并开启服务（mac命令：mongod --dbpath "/usr/local/var/mongodb" （前提是没有修改默认路径））
克隆远程库

git clone https://github.com/wangzhongjie/BlogCms.git
进入项目目录

cd BlogCms
安装依赖

npm install
进入服务器所在文件夹并运行服务器

cd server
node server
打开浏览器输入http://localhost:3300/