#### 安装kubeadm集群
##### 安装docker
```shell
# 删除docker
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
# 安装依赖
yum install -y yum-utils device-mapper-persistent-data lvm2
# 添加yum源
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# 安装docker
yum makecache fast
yum install -y docker-ce
systemctl start docker
# 添加docker配置
cat >> /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": ["http://hub-mirror.c.163.com"],
  "log-driver": "json-file",

}
EOF
```
##### 安装kubeadm
```shell
# 下载离线包
yum install -y wget
wget -c https://sealyun.oss-cn-beijing.aliyuncs.com/free/kube1.15.0.tar.gz
wget -c https://github.com/fanux/sealos/releases/download/v2.0.4/sealos
chmod +x sealos
# 安装HPA
sealos init --master 192.168.174.134 \
    --master 192.168.0.3 \
    --master 192.168.0.4 \              
    --node 192.168.0.5 \                 
    --user root \                        
    --passwd your-server-password \      
    --version v1.14.1 \
    --pkg-url /root/kube1.14.1.tar.gz  
# 安装单节点
sealos init --master 192.168.174.134 \
    --node 192.168.174.134 \                 
    --user root \                        
    --passwd 123456 \      
    --version v1.15.0 \
    --pkg-url /root/kube1.15.0.tar.gz 
```