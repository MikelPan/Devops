### 配置磁盘
```shell
pvcreate /dev/vdb1
vgcreate data /dev/vdb1
lvremote /dev/data/datalv
lvremote /dev/data/worklv
lvcreate /dev/data/worklv
lvcreate /dev/data/datalv

mkfs -t xfs /dev/data/datalv
mkfs -t xfs /dev/data/worklv

mkdir /data
mkdir /apps

mount /dev/data/datalv /data
mount /dev/data/worklv /apps

blikd /dev/data/datalv 
echo "UUID=  /data  xfs  defaults 1 1" >> /etc/fstab
echo "UUID=  /apps  xfs  defaults 1 1" >> /etc/fstab
```


### 配置主机名
```shell

hostnamectl set-hostname k8s-master01
hostnamectl set-hostname k8s-master02
hostnamectl set-hostname k8s-master03
hostnamectl set-hostname k8s-node01
#修改/etc/hosts
cat >> /etc/hosts << EOF
192.168.92.10 k8s-master01
192.168.92.11 k8s-master02
192.168.92.12 k8s-master03
192.168.92.13 k8s-node01
EOF
```

###  开启firewalld防火墙并允许所有流量
```shell
systemctl start firewalld && systemctl enable firewalld
firewall-cmd --set-default-zone=trusted
firewall-cmd --complete-reload
```
### 关闭selinux
```shell
sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config && setenforce 0
```

### 关闭swap
```shell
swapoff -a
yes | cp /etc/fstab /etc/fstab_bak
cat /etc/fstab_bak | grep -v swap > /etc/fstab
```

###  安装chron
```shell
yum install -y chrony
cp /etc/chrony.conf{,.bak}
```
###  注释默认ntp服务器
```shell
sed -i 's/^server/#&/' /etc/chrony.conf
```
###  指定上游公共 ntp 服务器
```shell
cat >> /etc/chrony.conf << EOF
server 0.asia.pool.ntp.org iburst
server 1.asia.pool.ntp.org iburst
server 2.asia.pool.ntp.org iburst
server 3.asia.pool.ntp.org iburst
EOF
```

### 设置时区
```shell
timedatectl set-timezone Asia/Shanghai
```
### 重启chronyd服务并设为开机启动：
```shell
systemctl enable chronyd && systemctl restart chronyd
```

### 验证,查看当前时间以及存在带*的行
```shell
timedatectl && chronyc sources


在所有的Kubernetes节点执行以下脚本（若内核大于4.19替换nf_conntrack_ipv4为nf_conntrack）:
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
```

###  安装依赖软件包
```shell
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
```
### 创建ha
```shell
mkdir -p /data/lb
cat > /data/lb/start-haproxy.sh << "EOF"
#!/bin/bash
MasterIP1=192.168.92.10
MasterIP2=192.168.92.11
MasterIP3=192.168.92.12
MasterPort=6443

docker run -d --restart=always --name HAProxy-K8S -p 6444:6444 \
        -e MasterIP1=$MasterIP1 \
        -e MasterIP2=$MasterIP2 \
        -e MasterIP3=$MasterIP3 \
        -e MasterPort=$MasterPort \
        wise2c/haproxy-k8s
EOF

cat > /data/lb/start-keepalived.sh << "EOF"
#!/bin/bash
VIRTUAL_IP=192.168.92.30
INTERFACE=ens33
NETMASK_BIT=24
CHECK_PORT=6444
RID=10
VRID=160
MCAST_GROUP=224.0.0.18

docker run -itd --restart=always --name=Keepalived-K8S \
        --net=host --cap-add=NET_ADMIN \
        -e VIRTUAL_IP=$VIRTUAL_IP \
        -e INTERFACE=$INTERFACE \
        -e CHECK_PORT=$CHECK_PORT \
        -e RID=$RID \
        -e VRID=$VRID \
        -e NETMASK_BIT=$NETMASK_BIT \
        -e MCAST_GROUP=$MCAST_GROUP \
        wise2c/keepalived-k8s
EOF

sh /data/lb/start-haproxy.sh && sh /data/lb/start-keepalived.sh
```

### 安装kubeadm
```shell

cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

#安装kubeadm、kubelet、kubectl,注意这里默认安装当前最新版本v1.14.1:
yum install -y kubeadm kubelet kubectl
systemctl enable kubelet && systemctl start kubelet


kubeadm config print init-defaults > kubeadm-config.yaml

apiVersion: kubeadm.k8s.io/v1beta1
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: abcdef.0123456789abcdef
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 192.168.92.10
  bindPort: 6443
nodeRegistration:
  criSocket: /var/run/dockershim.sock
  name: k8s-master01
  taints:
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
---
apiServer:
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta1
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controlPlaneEndpoint: "192.168.92.30:6444"
controllerManager: {}
dns:
  type: CoreDNS
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: registry.aliyuncs.com/google_containers
kind: ClusterConfiguration
kubernetesVersion: v1.14.1
networking:
  dnsDomain: cluster.local
  podSubnet: "10.244.0.0/16"
  serviceSubnet: 10.96.0.0/12
scheduler: {}

---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
featureGates:
  SupportIPVSProxyMode: true
mode: ipvs


kubeadm init --config=kubeadm-config.yaml --experimental-upload-certs | tee kubeadm-init.log

cat << EOF >> ~/.bashrc
export KUBECONFIG=/etc/kubernetes/admin.conf
EOF
source ~/.bashrc

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
cat kube-flannel.yml | grep image
cat kube-flannel.yml | grep 10.244
sed -i 's#quay.io/coreos/flannel:v0.11.0-amd64#willdockerhub/flannel:v0.11.0-amd64#g' kube-flannel.yml
kubectl apply -f kube-flannel.yml


kubectl apply -f \
https://docs.projectcalico.org/v3.6/getting-started/kubernetes/installation/hosted/kubernetes-datastore/calico-networking/1.7/calico.yaml

kubeadm join 192.168.92.30:6444 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:c0a1021e5d63f509a0153724270985cdc22e46dc76e8e7b84d1fbb5e83566ea8 \
    --experimental-control-plane --certificate-key 52f64a834454c3043fe7a0940f928611b6970205459fa19cb1193b33a288e7cc

kubeadm join 192.168.92.30:6444 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:c0a1021e5d63f509a0153724270985cdc22e46dc76e8e7b84d1fbb5e83566ea8

# 修改msater其他节点的ip指向
sed -i 's@server: https://xxxxx:6443@server: https://xxxx:8443@g' /etc/kubernetes/{admin.conf,kubelet.conf,kube-controller-manager.conf,kube-scheduler.conf}

systemctl daemon-reload
systemctl  restart docker kubelet

# 修改node节点的ip指向
sed -i 's@server: https://xxxx:6443@server: https://apiserver.cluster.local:6443@g' /etc/kubernetes/admin.conf

systemctl daemon-reload 
systemctl  restart docker kubelet

kubectl -n kube-system exec etcd-k8s-master01 -- etcdctl \
	--endpoints=https://192.168.92.10:2379 \
	--ca-file=/etc/kubernetes/pki/etcd/ca.crt \
	--cert-file=/etc/kubernetes/pki/etcd/server.crt \
	--key-file=/etc/kubernetes/pki/etcd/server.key cluster-health

# master节点允许调度
kubectl taint node k8s-master node-role.kubernetes.io/master-
# master 节点不许与调度
kubectl taint node k8s-master node-role.kubernetes.io/master=""

```

