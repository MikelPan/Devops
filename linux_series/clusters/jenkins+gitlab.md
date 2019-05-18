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
yum install -y java-1.8.0-openjdk-devel
cat >> /etc/profile <<EOF
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64
export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar 
export PATH=$JAVA_HOME/jre/bin:${PATH}
EOF
source /etc/profile
# 安装maven环境
wget http://mirror.bit.edu.cn/apache/maven/maven-3/3.6.1/binaries/apache-maven-3.6.1-bin.tar.gz
tar zxvf apache-maven-3.6.1-bin.tar.gz -C /usr/local/src 
mv /usr/local/src/apache-maven-3.6.1 /usr/local/apache-maven-3.6.1
echo "PATH=$PATH:/usr/local/apache-maven-3.6.1/bin" >>/etc/profile
source /etc/profile
# 修改maven仓库
   <localRepository>/root/mvnproject/repo</localRepository>
   <mirror>
      <id>nexus-aliyun</id>
      <mirrorOf>*</mirrorOf>
      <name>Nexus aliyun</name>
      <url>http://maven.aliyun.com/nexus/content/groups/public</url>
    </mirror>
# 安装jenkins
wget http://ftp-chi.osuosl.org/pub/jenkins/war-stable/2.164.3/jenkins.war
# jenkins开机启动
在jenkins目录下创建启动脚本，和编写systemd启动文件
mkdir /root/.jenkins/scripts
cd /root/.jenkins/scripts/ touch start.sh stop.sh
cat > start.sh <<EOF
#!/bin/bash
java -jar /root/sofeware/jenkins.war --httpPort=8888 & > /root/.jenkins/logs/start.log/start.log &
EOF
cat > stop.sh <<EOF
#!/bin/bash
pid=`ps aux | grep -v grep | grep jenkins | awk '{print $2}'`
kill -9 $pid
EOF
chmod +X start.sh stop.sh
cat > /usr/lib/systemd/system/jenkins.service <<EOF
[Unit]
Description=jenkins
After=syslog.target network.target

[Service]
Type=forking
ExecStart=/root/.jenkins/scripts/start.sh
ExecStop=/root/.jenkins/scripts/stop.sh
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
systemctl enable jenkins
systemctl start jenkins
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
                sh "mvn clean package"
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
#### 四、maven编译
```shell
# 创建maven项目
mkdir -p /root/mvnproject/mvn01 && cd /root/mvnproject/mvn01
vim pom.xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0  http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <!--所有的Maven项目都必须配置这四个配置项-->
    <modelVersion>4.0.0</modelVersion>
    <!--groupId指的是项目名的项目组，默认就是包名-->
    <groupId>com.plyx.mvn01</groupId>
    <!--artifactId指的是项目中的某一个模块，默认命名方式是"项目名-模块名"-->
    <artifactId>mvn01-model</artifactId>
    <!--version指的是版本，这里使用的是Maven的快照版本-->
    <version>SNAPSHOT-0.0.1</version>
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactID>junit</artifactID>
            <version>4.10</version>
        </dependency>
    </dependencies>
</project>
mkdir -p src/{main,test}/java/com/plyx/mvn01/model
```
