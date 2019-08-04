### go ubuntu安装
```shell
# 添加依赖
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:gophers/go
sudo apt-get update
sudo apt-get install -y git-core mercurial
# 安装go
wget https://dl.google.com/go/go1.12.7.linux-amd64.tar.gz
sudo tar -xzf go1.12.7.linux-amd64.tar.gz -C /usr/local
# 配置环境变量
vim /etc/profile
export GOROOT=/usr/local/go
export GOBIN=$GOROOT/bin
export GOPATH=/opt/go
export PATH=$PATH:$GOBIN
```
### go 模块使用
```shell
# 开启module
export GO111MODULE=on
# 添加代理
export GOPROXY=https://mirrors.aliyun.com/goproxy/
# 使用module
mkdir $GOPATH/github.com/plyx/website
cd $GOPATH/github.com/plyx/website
```