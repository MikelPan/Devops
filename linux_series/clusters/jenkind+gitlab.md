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
#### 二、安装gitlab
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
#### 三、安装jenkins
```shell
# 安装java环境
yum install -y java-1.8.0-openjdk
# 安装maven环境
wget http://mirror.bit.edu.cn/apache/maven/maven-3/3.6.1/binaries/apache-maven-3.6.1-bin.tar.gz
tar zxvf apache-maven-3.6.1-bin.tar.gz -C /usr/local/src 
mv /usr/local/src/apache-maven-3.6.1 /usr/local/apache-maven-3.6.1
echo "PATH=$PATH:/usr/local/apache-maven-3.6.1/bin" >>/etc/profile
source /etc/profile
wget http://ftp-chi.osuosl.org/pub/jenkins/war-stable/2.164.3/jenkins.war
java -jar jenkins.war --httpPort=8888 &
```
**编写jenkins pipeline语法**
```groovy
#!groovy
pipeline {
    agent any
    
    environment {
        RESITORY="http://gitlab.plyx.site:8080/mikel/mikelservice.git"
        MODULE="zookeeper-test"
        SCRIPT_DIR="/root/scripts"
    }
    
    stages {
        
        stage ('获取代码') {
            steps {
                echo "start frech get code from git:${RESITORY}"
                deleteDir()
                git "${RESITORY}"
            }
            
        stage ('编译+单元测试') {
            steps {
                echo "start compile"
                sh "mvn -U -pl ${MODULE} -am clean pakeage"
            }
        }
        
        stage ('构建镜像') {
            steps {
                echo "start build image"
                sh "${SCRTPT_DIR}/build-image.sh"
            }
        }
    }
}
```
