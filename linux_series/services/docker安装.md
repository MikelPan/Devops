#### 一、docker yum安装
```shell
# docker 卸载
yum remove docker \
           docker-client \
           docker-client-latest \
           docker-common \
           docker-latest \
           docker-latest-logrotate \
           docker-logrotate \
           docker-selinux \
           docker-engine-selinux \
           docker-engine

rm -rf /etc/systemd/system/docker.service.d
rm -rf /var/lib/docker
rm -rf /var/run/docker
# 安装docker
yum -y install yum-utils
yum-config-manager --add-repo  https://download.docker.com/linux/centos/docker-ce.repo
yum makecache fast
yum install -y docker-ce
cat > /etc/docker/daemon.json <<EOF
{"data-root": "/data/docker","registry-mirrors": ["http://9b2cd203.m.daocloud.io"]}
EOF
iptables -P FORWARD ACCEPT
```
#### 二、docker 二进制安装
```shell
# 下载docker
wget https://download.docker.com/linux/static/stable/x86_64/docker-18.09.6.tgz
tar zxvf docker-18.09.6.tgz -C /usr/local/src
mv /usr/local/src/docker/* /usr/bin
systemctl enable docker
systemctl start docker
cat > /etc/docker/daemon.json <<EOF
{"data-root": "/data/docker","registry-mirrors": ["http://9b2cd203.m.daocloud.io"]}
EOF
iptables -P FORWARD ACCEPT
```
#### 三、docker-compose安装
```shell
自动下载
curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
# 手动下载
wget -c https://github.com/docker/compose/releases/download/1.24.0/docker-compose-Linux-x86_64
```