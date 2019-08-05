#### 一、安装docker环境
```shell
 下载docker
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
#### 二、docker安装gitlab
```shell
docker pull gitlab/gitlab-ce
mkdir /data/gitlab
cat > /data/gitlab/start.sh <<EOF
#!/bin/bash
HOST_NAME=gitlab.plyx.site
GITLAB_DIR=/data/gitlab
docker stop gitlab
docker rm gitlab
docker run -d \
    --hostname ${HOST_NAME} \
    -p 443:443 80:80 2222:22 \
    --name gitlab \
    -v ${GITLAB_DIR}/config:/etc/gitlab \
    -v ${GITLAB_DIR}/data:/var/opt/gitlab \
    -v ${GITLAB_DIR}/log:/var/log/gitlab \
    gitlab/gitlba-ce
EOF
# 添加host解析
127.0.0.1 gitlab.plyx.site
# 修改配置文件
gitlab_rails['gitlab_shell_ssh_port'] = 2222
```
#### 三、yum安装gitlab
```shell
# 安装依赖
准备一台linux服务器，内存为4G
yum install -y git vim gcc glibc-static telnet
yum install -y curl policycoreutils-python openssh-server
systemctl enable sshd
systemctl start sshd
yum install postfix
systemctl enable postfix
systemctl start postfix
# 设置gitlab安装源
新建/etc/yum.repos.d/gitlab-ce.repo 内容为
[gitlab-ce]
name=Gitlab CE Repository
baseurl=https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el$releasever/
gpgcheck=0
enabled=1
# 使用域名方式安装
EXTERNAL_URL="http://gitlab.plyx.site" yum install -y gitlab-ce
# 重新配置
gitlab-ctl reconfigure
```
#### 四、安装dns服务器
```shell
# 启动dnsmq
在另外一台机器上 192.168.174.201 安装dns服务
docker run -d -p 53:53/tcp -p 53:53/udp --cap-add=NET_ADMIN --name dns-server andyshinn/dnsmasq
# 进入到容器修改配置
docker exec -it dns-server bash
vim /etc/resolv.dnsmasq
nameserver 114.114.114.114
nameserver 8.8.8.8
vim /etc/dnsmasqhosts
192.168.174.200 gitlab.plyx.site
# 重启容器
docker restart dns-server
# 修改gitlab dns
vim /etc/resolv.conf
nameserver 192.168.174.201
```
#### 五、搭建私有仓库registry
```shell
# dns添加registry域名
vim /etc/dnsmasqhosts
192.168.174.200 gitlab.plyx.site
192.168.174.202 registry.plyx.site
# 启动docker registry
docker run -d -v /opt/registry:/var/lib/registry -p 5000:5000 --restart=always --name registry registry:2
# 添加docker配置
vim /etc/docker/daemon.json
{"insecure-registries":["registry.plyx.site:5000"]}
# 公网拉取镜像 推送到registry上
docker pull busybox
docker tag busybox registry.plyx.site:5000/busybox
docker push registry.plyx.site:5000/busybox
```
#### 六、安装gitlab-ci服务器
```shell
# 安装gitlab-ci running服务器
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-ci-multi-runner/script.rpm.sh | bash
yum install gitlab-ci-multi-runner -y
# 设置docker权限
usermod -aG docker gitlab-runner
systemctl restart docker
systemctl restart gitlab-ci-multi-runner
```





