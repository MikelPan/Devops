#### 一、python安装
**安装步骤**:
- 下载tar包
- 解压文件
- 添加环境变量
- 编译安装
- 更换系统python版本
- 配置yum
```shell
1、安装get
yum install -y wget
2、下载tar包
wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
3、解压文件
tar zxvf Python-3.7.3.tgz -C /usr/local/src
mkidr /usr/local/python
4、添加环境变量
echo "export PATH=$PATH:/usr/local/python/bin" >> /etc/profile
source /etc/profile
5、编译安装
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc-c++ make libffi-devel
cd /usr/local/src/Python-3.7.3 && ./configure --prefix=/usr/local/python
make -j 3 && make install
6、更换系统python版本
mv /usr/bin/python /usr/bin/python2.7.5
ln -s /usr/local/python/bin/python3.7 /usr/bin/python
7、配置yum
sed -i 's@#!/usr/bin/python@#!/usr/bin/python2.7@g' /usr/bin/yum
sed -i 's@#!/usr/bin/python@#!/usr/bin/python2.7@g' /usr/libexec/urlgrabber-ext-down
```
------
#### 二、python虚拟环境
**安装步骤**
- 安装virtualenv
- 安装virtualenvwrapper
**1、安装virtualenv**
```shell
1、安装pip
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
2、安装virtualenv
pip3 install virtualenv
3、指定虚拟环境
virtualenv -p /usr/local/python/bin/python3 demo
4、启动虚拟环境
cd demo && source /demo/bin/activate
5、退出虚拟环境
deactivate
```
**2、安装virtualenvwrapper**
```shell
1、安装virtualenvwrapper
pip3 install virtualenvwrapper
2、创建虚拟机
mkvirtualenv demo -p /usr/local/python/bin/python3
3、列出虚拟机
lsvirtualenv
4、启动虚拟机
workon demo
5、删除虚拟机
rmvirtualenv demo
6、离开虚拟环境
deactivate
```
