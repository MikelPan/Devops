#!/bin/bash
parms=$1
java_install(){
yum install -y java-1.8.0-openjdk-devel
}
java_envconfig(){
cat >> /etc/profile <<EOF
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64
export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$JAVA_HOME/jre/bin:${PATH}
EOF
source /etc/profile
}
maven_install(){
wget http://mirror.bit.edu.cn/apache/maven/maven-3/3.6.1/binaries/apache-maven-3.6.1-bin.tar.gz -P /root/sofeware
tar zxvf /root/sofeware/apache-maven-3.6.1-bin.tar.gz -C /usr/local/src
mv /usr/local/src/apache-maven-3.6.1 /usr/local/apache-maven-3.6.1
echo "PATH=$PATH:/usr/local/apache-maven-3.6.1/bin" >>/etc/profile
source /etc/profile
}
jenkins_install(){
wget http://ftp-chi.osuosl.org/pub/jenkins/war-stable/2.164.3/jenkins.war -P /root/sofeware
java -jar /root/sofeware/jenkins.war --httpPort=8888 &
}
jenkins_authstart(){
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
systemctl restart jenkins
}
main(){
case ${parms} in
    java_install)
    java_install
    ;;
    java_envconfig)
    java_envconfig
    ;;
    maven_install)
    maven_install
    ;;
    jenkins_install)
    jenkins_install
    ;;
    jenkins_autostart)
    jenkins_autostart
    ;;
    *)
    echo "Usge please input jenkins_install (java_install | java_envconfig  | maven_install | jenkins_install | jenkins_autostart)"
    ;;
esac
}
main
