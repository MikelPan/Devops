### 配置主机名
hostnamectl set-hostname k8s-master01
#修改/etc/hosts
cat >> /etc/hosts << EOF
172.18.28.157 k8s-master01
172.18.28.158 k8s-master02
172.18.28.159 k8s-master03
172.18.28.160 k8s-node01
EOF
###  开启firewalld防火墙并允许所有流量
systemctl disable firewalld && systemctl stop firewalld
### 关闭selinux
sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config && setenforce 0
### 关闭swap
swapoff -a
yes | cp /etc/fstab /etc/fstab_bak
cat /etc/fstab_bak | grep -v swap > /etc/fstab
###  安装chron
yum install -y chrony
cp /etc/chrony.conf{,.bak}
###  注释默认ntp服务器
sed -i 's/^server/#&/' /etc/chrony.conf
###  指定上游公共 ntp 服务器
cat >> /etc/chrony.conf << EOF
server 0.asia.pool.ntp.org iburst
server 1.asia.pool.ntp.org iburst
server 2.asia.pool.ntp.org iburst
server 3.asia.pool.ntp.org iburst
EOF
### 设置时区
timedatectl set-timezone Asia/Shanghai
### 重启chronyd服务并设为开机启动：
systemctl enable chronyd && systemctl restart chronyd
### 验证,查看当前时间以及存在带*的行
timedatectl && chronyc sources
cat > /etc/sysconfig/modules/ipvs.modules <<EOF
#!/bin/bash
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4
EOF
#执行脚本
chmod 755 /etc/sysconfig/modules/ipvs.modules && bash /etc/sysconfig/modules/ipvs.modules && lsmod | grep -e ip_vs -e nf_conntrack_ipv4
#安装相关管理工具
yum install ipset ipvsadm -y
cat > /etc/sysctl.d/k8s.conf <<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_nonlocal_bind = 1
net.ipv4.ip_forward = 1
vm.swappiness=0
EOF
sysctl --system
###  安装依赖软件包
yum install -y yum-utils device-mapper-persistent-data lvm2
# 添加Docker repository，这里改为国内阿里云yum源
yum-config-manager \
  --add-repo \
  http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# 安装docker-ce
yum update -y && yum install -y docker-ce
## 创建 /etc/docker 目录
mkdir /etc/docker
# 配置 daemon.
cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ],
  "registry-mirrors": ["https://uyah70su.mirror.aliyuncs.com"]
}
EOF
#注意，由于国内拉取镜像较慢，配置文件最后追加了阿里云镜像加速配置。
mkdir -p /etc/systemd/system/docker.service.d
# 重启docker服务
systemctl daemon-reload && systemctl restart docker && systemctl enable docker