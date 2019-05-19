

### kubernetes部署实践文档

#### 00、基础环境安装

##### 1、部署规划

```shell
# ip地址
kubernetes_node1:192.168.174.10
kubernetes_node2:192.168.174.11
# 主机名
kubernetes_node1:node1
kubernetes_node2:node2
# 磁盘规划
kubernetes_node1: 
	1、/data/docker  # docker根目录
	2、/work/kubernetes_deploy  # kubenetes 部署目录
	3、/work/kubernetes_deploy/ssl # kubernetes ssl 证书目录
	4、
```

##### 2、每个节点安装依赖

```shell
# 配置IP地址
cat >> /etc/sysconfig/network-scripts/ifcfg-ens33 <<EOF   # kubernetes_node1
IPADDR=192.168.174.10
NETMASK=255.255.255.0
GATEWAY=192.168.174.2
DNS1=8.8.8.8
EOF
cat >> /etc/sysconfig/network-scripts/ifcfg-ens33 <<EOF   # kubernetes_node2
IPADDR=192.168.174.10
NETMASK=255.255.255.0
GATEWAY=192.168.174.2
DNS1=8.8.8.8
EOF
# 配置主机名
hostnamectl set-hostname node1  # kubernetes_node1
hostnamectl set-hostname node2  # kubernetes_node2
# 添加hosts
cat >> /etc/hosts <<EOF
192.168.174.10 node1
192.168.174.11 node2
EOF
scp /etc/hosts root@192.168.174.11:/etc/hosts  # 拷贝到其他节点
# 关闭防火墙
systemctl stop firewalld
systemctl disable firewalld
# 关闭selinux
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config 
# 安装软件包
yum install epel-release vim git lrzsz htop atop net-tools tcpdump wget -y
yum -y update
yum makecache fast
# 删除不要的默认安装
yum erase firewalld firewalld-filesystem python-firewall -y
```

##### 3、安装python环境

```shell
# 下载tar包
mkdir /root/sofeware && cd /root/sofeware
wget -c https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
# 解压文件
tar zxvf Python-3.7.3.tgz -C /usr/local/src && mkdir /usr/local/python
# 添加环境变量
echo "export PATH=$PATH:/usr/local/python/bin" >> /etc/profile && source /etc/profile
# 编译安装
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc-c++ make libffi-devel
cd /usr/local/src/Python-3.7.3 && ./configure --prefix=/usr/local/python
make -j 3 && make install
# 更换系统python版本
mv /usr/bin/python /usr/bin/python2.7.5
ln -s /usr/local/python/bin/python3.7 /usr/bin/python
# 配置yum
sed -i 's@#!/usr/bin/python@#!/usr/bin/python2.7@g' /usr/bin/yum
sed -i 's@#!/usr/bin/python@#!/usr/bin/python2.7@g' /usr/libexec/urlgrabber-ext-down
```

##### 4、在deploy节点安装ansible

```shell
# yum 安装
yum -y install ansible
# pip 安装 yum
pip install pip --upgrade -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
pip install --no-cache-dir ansible -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

##### 5、deploy部署ssh-key

```shell
# 创建ssh-key
ssh-keygen -t rsa -C "plyx_46204@126.com"
# 拷贝到各节点
ssh-copy-id node1
ssh-copy-id node2
# 配置ansible hosts
cat >> /etc/ansible/hosts <<EOF
[node]
192.168.174.10 node1
192.168.174.11 node2
EOF
# 验证ansible
ansible node -m ping
192.168.174.10 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.174.11 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```

##### 6、deploy部署k8s

```shell
# 克隆项目到本地
mkdir /root/kubernetes_deploy && cd /root/kubernetes_deploy
git clone https://github.com/gitplyx/kubeasz.git
cp -r /root/kubernetes_deploy/kubeasz/* ./ && rm -rf /root/kubernetes_deploy/kubeasz
# 下载已打包好的binaries，并且解压缩到/root/kubernetes_deploy/bin目录
# 如果你有合适网络环境也可以按照/down/download.sh自行从官网下载各种tar包到 ./down目录，并执行download.sh
cd /root/kubernetes_deploy/
cp example/hosts.m-masters.example /etc/ansible/hosts
# 根据上文实际规划修改此hosts文件
vim hosts
---------------------------------------start--------------------------------------------
# 集群部署节点：一般为运行ansible 脚本的节点
# 变量 NTP_ENABLED (=yes/no) 设置集群是否安装 chrony 时间同步
[deploy]
192.168.174.10 NTP_ENABLED=no

# etcd集群请提供如下NODE_NAME，请注意etcd集群必须是1,3,5,7...奇数个节点
[etcd]
192.168.174.10 NODE_NAME=etcd1

[kube-master]
192.168.174.10

[kube-node]
192.168.174.10
192.168.174.11

# 参数 NEW_INSTALL：yes表示新建，no表示使用已有harbor服务器
# 如果不使用域名，可以设置 HARBOR_DOMAIN=""
[harbor]
192.168.174.10 HARBOR_DOMAIN="harbor.plyx.site" NEW_INSTALL=yes

#【可选】外部负载均衡，用于自有环境负载转发 NodePort 暴露的服务等
[ex-lb]
#192.168.174.10 LB_ROLE=backup EX_VIP=192.168.174.200
#192.168.174.11 LB_ROLE=master EX_VIP=192.168.174.200

[all:vars]
# ---------集群主要参数---------------
#集群部署模式：allinone, single-master, multi-master
DEPLOY_MODE=single-master

#集群 MASTER IP，自动生成
MASTER_IP="{{ groups['kube-master'][0] }}"
KUBE_APISERVER="https://{{ MASTER_IP }}:6443"

# 集群网络插件，目前支持calico, flannel, kube-router, cilium
#CLUSTER_NETWORK="flannel"
CLUSTER_NETWORK="calicao"

# 服务网段 (Service CIDR），注意不要与内网已有网段冲突
SERVICE_CIDR="10.68.0.0/16"

# POD 网段 (Cluster CIDR），注意不要与内网已有网段冲突
CLUSTER_CIDR="172.20.0.0/16"

# 服务端口范围 (NodePort Range)
NODE_PORT_RANGE="20000-40000"

# kubernetes 服务 IP (预分配，一般是 SERVICE_CIDR 中第一个IP)
CLUSTER_KUBERNETES_SVC_IP="10.68.0.1"

# 集群 DNS 服务 IP (从 SERVICE_CIDR 中预分配)
CLUSTER_DNS_SVC_IP="10.68.0.2"

# 集群 DNS 域名
CLUSTER_DNS_DOMAIN="cluster.local."

# ---------附加参数--------------------
#默认二进制文件目录
bin_dir="/opt/kube/bin"

#证书目录
ca_dir="/etc/kubernetes/ssl"

#部署目录，即 ansible 工作目录
base_dir="/root/kubernetes-deploy"
-------------------------------------------end------------------------------------------
```

##### 7、开始安装集群

```shell
# 分布安装
ansible-playbook 01.prepare.yml
#注意，如果后台进程有yum在运行，该命令会无限等待，不会超时退出并打印出错误，这个是Bug，需要手工将yum进程杀死。因为该任务里面需要将firewalld, firewalld-system，python-firewall三个组件使用yum命令删除掉，yum命令的缺陷
ansible-playbook 02.etcd.yml
ansible-playbook 03.kubectl.yml
ansible-playbook 04.docker.yml
ansible-playbook 05.kube-master.yml
ansible-playbook 06.kube-node.yml
ansible-playbook 07.calico.yml     # 网络模式选择calico   运行此脚本
ansible-playbook 07.flannel.yml    # 网络模式选择flannel  运行此脚本
# 一步安装
ansible-playbook 90.setup.yml 
```

#### 01、创建CA证书和环境配置

------

本步骤[01.prepare.yml](https://github.com/gitplyx/kubeasz/blob/master/01.prepare.yml)主要完成CA证书创建、分发、环境变量、负载均衡配置等 

##### 1、创建CA证书和秘钥

```shell
roles/deploy
├── tasks
│   └── main.yml
└── templates
    ├── ca-config.json.j2
    └── ca-csr.json.j2
```

- `etcd` 节点需要标识自己监听服务的server cert，也需要client cert与`etcd`集群其他节点交互，当然可以分别指定2个证书，这里为简化使用一个peer 证书
- `kube-apiserver` 需要标识apiserver服务的server cert，也需要client cert 从而操作`etcd`集群，这里为简化使用一个peer 证书
- `kubectl` `calico` `kube-proxy` 只需要 client cert，因此证书请求中 hosts 字段可以为空
- `kubelet` 证书比较特殊，不是手动生成，它由node节点`TLS BootStrap` 向`apiserver`请求，由master节点的`controller-manager` 自动签发，包含一个client cert 和一个server cert

##### 2、创建CA配置文件

```shell
ca-csr.json.j2
{
  "signing": {
    "default": {
      "expiry": "87600h"
    },
    "profiles": {
      "kubernetes": {
        "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
        ],
        "expiry": "87600h"
      }
    }
  }
}
```

- `ca-config.json`：可以定义多个 profiles，分别指定不同的过期时间、使用场景等参数；这里为了方便使用 `kubernetes` 这个profile 签发三种不同类型证书

- `signing`：表示该证书可用于签名其它证书；生成的 ca.pem 证书中 `CA=TRUE`；
- `server auth`：表示 client 可以用该 CA 对 server 提供的证书进行验证；
- `client auth`：表示 server 可以用该 CA 对 client 提供的证书进行验证；

##### 3、创建 CA 证书签名请求

```shell
{
  "CN": "kubernetes",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "HangZhou",
      "L": "XS",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
```

##### 3、生成CA 证书和私钥

```shell
cfssl gencert -initca ca-csr.json | cfssljson -bare ca
```

- 注意整个集群只能有一个CA证书和配置文件，所以下一步要分发给每一个节点，包括calico/node也需要使用，`ansible` 角色(role) `prepare` 会完成CA 证书分发，所以把ca 证书相关先复制到 `roles/prepare/files/`

**准备分发证书**

```shell
# 准备分发 CA证书
- name: copy ca to nodes
  copy: src={{ ca_dir }}/{{ item }} dest={{ base_dir }}/roles/prepare/files/{{ item }} force=no
  with_items:
  - ca.pem
  - ca-key.pem
  - ca.csr
  - ca-config.json
```

- force=no 保证整个安装的幂等性，如果已经生成过CA证书，就使用已经存在的CA，可以多次运行 `ansible-playbook 90.setup.yml`
- 如果确实需要更新CA 证书，删除/roles/prepare/files/ca* 可以使用新CA 证书

##### 4、kubedns.yml 文件生成

- kubedns.yaml文件中部分参数(CLUSTER_DNS_SVC_IP, CLUSTER_DNS_DOMAIN)根据hosts文件设置而定，因此需要用template模块替换参数
- 运行本步骤后，在 manifests/kubedns目录下生成 kubedns.yaml 文件，以供后续部署时使用

```shell
roles/prepare/
├── files
│   ├── 95-k8s-sysctl.conf
│   ├── ca-config.json
│   ├── ca.csr
│   ├── ca-csr.json
│   ├── ca-key.pem
│   └── ca.pem
└── tasks
    └── main.yml
```

**执行步骤说明**

1. 首先创建一些基础文件目录
2. 修改环境变量，把{{ bin_dir }} 添加到$PATH，需要重新登陆 shell生效
3. 把证书工具 CFSSL下发到指定节点
4. 把CA 证书相关下发到指定节点的 {{ ca_dir }} 目录
5. 最后设置基础操作系统软件和系统参数，请阅读脚本中的注释内容

##### 5、LB负载均衡配置

```shell
roles/lb
├── tasks
│   └── main.yml
└── templates
    ├── haproxy.cfg.j2
    ├── keepalived-backup.conf.j2
    └── keepalived-master.conf.j2
```

keepalived与haproxy配合，实现master的高可用过程如下： 

- 1.keepalived利用vrrp协议生成一个虚拟地址(VIP)，正常情况下VIP存活在keepalive的主节点，当主节点故障时，VIP能够漂移到keepalived的备节点，保障VIP地址可用性。
- 2.在keepalived的主备节点都配置相同haproxy负载配置，并且监听客户端请求在VIP的地址上，保障随时都有一个haproxy负载均衡在正常工作。并且keepalived启用对haproxy进程的存活检测，一旦主节点haproxy进程故障，VIP也能切换到备节点，从而让备节点的haproxy进行负载工作。
- 3.在haproxy的配置中配置多个后端真实kube-apiserver的endpoints，并启用存活监测后端kube-apiserver，如果一个kube-apiserver故障，haproxy会将其剔除负载池。

**安装haproxy**

此次脚本会自动安装，下面为手动安装方法

```shell
# yum安装
yum install -y haproxy
# 二进制安装
wget -c https://fossies.org/linux/misc/haproxy-1.9.8.tar.gz -P /root/sofeware && cd /root/sofeware 
tar zxvf haproxy-1.9.8.tar.gz -C /usr/local/src && cd /usr/local/src
make TARGET=linux2628 ARCH=x86_64 PREFIX=/usr/local/haproxy
make install PREFIX=/usr/local/haproxy
# 启动
/usr/local/haproxy/sbin/haproxy -f /usr/local/haproxy/haproxy.cfg
```

**配置haproxy.cfg.j2**

```shell
global
        log /dev/log    local0
        log /dev/log    local1 notice
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin
        stats timeout 30s
        user haproxy
        group haproxy
        daemon
        nbproc 1

defaults
        log     global
        timeout connect 5000
        timeout client  50000
        timeout server  50000

listen kube-master
        bind 0.0.0.0:{{ MASTER_PORT }}
        mode tcp
        option tcplog
        balance source
        server s1 {{ LB_EP1 }}  check inter 10000 fall 2 rise 2 weight 1
        server s2 {{ LB_EP2 }}  check inter 10000 fall 2 rise 2 weight 1
```

各项配置说明：

- 名称 kube-master
- bind 监听客户端请求的地址/端口，保证监听master的VIP地址和端口，{{ MASTER_PORT }}与hosts里面设置对应
- mode 选择四层负载模式 (当然你也可以选择七层负载，请查阅指南，适当调整)
- balance 选择负载算法 (负载算法也有很多供选择)
- server 配置master节点真实的endpoits，必须与 [hosts文件](https://github.com/gitplyx/kubeasz/blob/master/example/hosts.m-masters.example)对应设置

**安装keeplived**

此次脚本会自动安装，下面为手动安装方法

```shell
# 安装依赖包
yum install -y net-tools psmisc
yum install -y net-snmp
yum install -y ipvsadm  keepalived

# 拷贝配置文件
cp /usr/share/doc/keepalived/samples/keepalived.conf.sample /etc/keepalived/keepalived.conf

# 编辑配置文件
vim /etc/keepalived/keepalived.conf
```

**配置主节点keeplived-master.conf.j2**

```shell
global_defs {
    router_id lb-master
}

vrrp_script check-haproxy {
    script "killall -0 haproxy"
    interval 5
    weight -30
}

vrrp_instance VI-kube-master {
    state MASTER
    priority 120
    dont_track_primary
    interface {{ LB_IF }}
    virtual_router_id 51
    advert_int 3
    track_script {
        check-haproxy
    }
    virtual_ipaddress {
        {{ MASTER_IP }}
    }
}
```

- vrrp_script 定义了监测haproxy进程的脚本，利用shell 脚本`killall -0 haproxy` 进行检测进程是否存活，如果进程不存在，根据`weight -30`设置将主节点优先级降低30，这样原先备节点将变成主节点。
- vrrp_instance 定义了vrrp组，包括优先级、使用端口、router_id、心跳频率、检测脚本、虚拟地址VIP等
- 特别注意 `virtual_router_id` 标识了一个 VRRP组，在同网段下必须唯一，否则出现 `Keepalived_vrrp: bogus VRRP packet received on eth0 !!!`类似报错

**配置备节点keeplived-backup.conf.j2**

```shell
global_defs {
    router_id lb-backup
}

vrrp_instance VI-kube-master {
    state BACKUP
    priority 110
    dont_track_primary
    interface {{ LB_IF }}
    virtual_router_id 51
    advert_int 3
    virtual_ipaddress {
        {{ MASTER_IP }}
    }
}
```

- 备节点的配置类似主节点，除了优先级和检测脚本，其他如 `virtual_router_id` `advert_int` `virtual_ipaddress`必须与主节点一致

**查看keeplived主备状态**

```shell
systemctl status haproxy 	# 检查进程状态
journalctl -u haproxy		# 检查进程日志是否有报错信息
systemctl status keepalived 	# 检查进程状态
journalctl -u keepalived	# 检查进程日志是否有报错信息
netstat -antlp|grep 8443	# 检查tcp端口是否监听
```

#### 02、安装etcd集群

------

创建文件目录：

```shell
roles/etcd
├── tasks
│   └── main.yml
└── templates
    ├── etcd-csr.json.j2
    |-- etcd.conf.j2
    └── etcd.service.j2 
```

kuberntes 系统使用 etcd 存储所有数据，是最重要的组件之一，注意 etcd集群只能有奇数个节点(1,3,5...)，本文档使用3个节点做集群 .

##### 1、创建etcd证书请求

```shell
# 创建证书请求文件etcd-csr.json.j2
{
  "CN": "etcd",
  "hosts": [
    "127.0.0.1",
    "{{ NODE_IP }}"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "GuangDong",
      "L": "ShenZhen",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
```

##### 2、创建证书和秘钥

```shell
cd /etc/etcd/ssl && {{ bin_dir }}/cfssl gencert \
        -ca={{ ca_dir }}/ca.pem \
        -ca-key={{ ca_dir }}/ca-key.pem \
        -config={{ ca_dir }}/ca-config.json \
        -profile=kubernetes etcd-csr.json | {{ bin_dir }}/cfssljson -bare etcd
```

##### 3、创建etcd.service.j2文件

```shell
[Unit]
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target
Documentation=https://github.com/coreos

[Service]
Type=notify
WorkingDirectory=/var/lib/etcd/
ExecStart={{ bin_dir }}/etcd 
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

##### 4、创建etcd.config.j2

```shell
# [member]
ETCD_NAME={{ NODE_NAME }}
ETCD_DATA_DIR="/data/etcd/default.etcd"
#ETCD_WAL_DIR=""
#ETCD_SNAPSHOT_COUNT="10000"
#ETCD_HEARTBEAT_INTERVAL="100"
#ETCD_ELECTION_TIMEOUT="1000"
ETCD_LISTEN_PEER_URLS="https://{{ NODE_IP }}:2380"
ETCD_LISTEN_CLIENT_URLS="https://127.0.0.1:2379,https://{{ NODE_IP }}:2379"
#ETCD_MAX_SNAPSHOTS="5"
#ETCD_MAX_WALS="5"
#ETCD_CORS=""
#
#[cluster]
ETCD_INITIAL_ADVERTISE_PEER_URLS="https://{{ NODE_IP }}:2380"
# if you use different ETCD_NAME (e.g. test), set ETCD_INITIAL_CLUSTER value for this name, i.e. "test=http://..."
ETCD_INITIAL_CLUSTER={{ ETCD_NODES }}
ETCD_INITIAL_CLUSTER_STATE={{ CLUSTER_STATE }}
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_ADVERTISE_CLIENT_URLS="https://{{ NODE_IP }}:2379"
#ETCD_DISCOVERY=""
#ETCD_DISCOVERY_SRV=""
#ETCD_DISCOVERY_FALLBACK="proxy"
#ETCD_DISCOVERY_PROXY=""
#
#[proxy]
#ETCD_PROXY="off"
#ETCD_PROXY_FAILURE_WAIT="5000"
#ETCD_PROXY_REFRESH_INTERVAL="30000"
#ETCD_PROXY_DIAL_TIMEOUT="1000"
#ETCD_PROXY_WRITE_TIMEOUT="5000"
#ETCD_PROXY_READ_TIMEOUT="0"
#
#[security]
#ETCD_CERT_FILE=""
#ETCD_KEY_FILE=""
#ETCD_CLIENT_CERT_AUTH="false"
#ETCD_TRUSTED_CA_FILE=""
#ETCD_PEER_CERT_FILE=""
#ETCD_PEER_KEY_FILE=""
#ETCD_PEER_CLIENT_CERT_AUTH="false"
#ETCD_PEER_TRUSTED_CA_FILE=""
ETCD_CERT_FILE="/etc/etcd/ssl/etcd.pem"
ETCD_KEY_FILE="/etc/etcd/ssl/etcd-key.pem"
ETCD_TRUSTED_CA_FILE="{{ca_dir}}/ca.pem"
ETCD_CLIENT_CERT_AUTH="true"
ETCD_PEER_CERT_FILE="/etc/etcd/ssl/etcd.pem"
ETCD_PEER_KEY_FILE="/etc/etcd/ssl/etcd-key.pem"
ETCD_PEER_TRUSTED_CA_FILE="{{ca_dir}}/ca.pem"
ETCD_PEER_CLIENT_CERT_AUTH="true"
#
#[logging]
ETCD_DEBUG="false"
# examples for -log-package-levels etcdserver=WARNING,security=DEBUG
ETCD_LOG_PACKAGE_LEVELS="etcdserver=DEBUG"
```

##### 5、启动etcd服务

```shell
systemctl daemon-reload && systemctl enable etcd && systemctl start etcd
```

##### 6、验证etcd服务

- systemctl status etcd 查看服务状态
- journalctl -u etcd 查看运行日志
- 在任一 etcd 集群节点上执行如下命令

```shell
# 根据hosts中配置设置shell变量 $NODE_IPS
export NODE_IPS="192.168.174.10"
$ for ip in ${NODE_IPS}; do
  ETCDCTL_API=3 /usr/local/bin/etcdctl \
  --endpoints=https://${ip}:2379  \
  --cacert=/etc/kubernetes/ssl/ca.pem \
  --cert=/etc/etcd/ssl/etcd.pem \
  --key=/etc/etcd/ssl/etcd-key.pem \
  endpoint health; done
```

预期结果 :

```shell
https://192.168.174.200:2379 is healthy: successfully committed proposal: took = 2.210885ms
```

#### 03、配置kubectl命令行工具

配置文件目录如下：

```
roles/kubectl
├── tasks
│   └── main.yml
└── templates
    └── admin-csr.json.j2
```

##### 1、准备kubectl使用的admin 证书签名请求 admin-csr.json.j2

```shell
{
  "CN": "admin",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "GuangDong",
      "L": "ShenZhen",
      "O": "system:masters",
      "OU": "System"
    }
  ]
}
```

##### 2、创建admin证书

```shell
cd {{ ca_dir }} && {{ bin_dir }}/cfssl gencert \
        -ca={{ ca_dir }}/ca.pem \
        -ca-key={{ ca_dir }}/ca-key.pem \
        -config={{ ca_dir }}/ca-config.json \
        -profile=kubernetes admin-csr.json | {{ bin_dir }}/cfssljson -bare admin
```

##### 3、创建 kubectl kubeconfig 文件

设置集群参数，指定CA证书和apiserver地址

```shell
{{ bin_dir }}/kubectl config set-cluster kubernetes \
        --certificate-authority={{ ca_dir }}/ca.pem \
        --embed-certs=true \
        --server={{ KUBE_APISERVER }}
```

设置客户端认证参数，指定使用admin证书和私钥

```shell
{{ bin_dir }}/kubectl config set-credentials admin \
        --client-certificate={{ ca_dir }}/admin.pem \
        --embed-certs=true \
        --client-key={{ ca_dir }}/admin-key.pem
```

设置上下文参数，说明使用cluster集群和用户admin

```shell
{{ bin_dir }}/kubectl config set-context kubernetes \
        --cluster=kubernetes --user=admin
```

设置默认上下文

```shell
{{ bin_dir }}/kubectl config use-context kubernetes
```

- 注意{{ }}中参数与ansible hosts文件中设置对应
- 以上生成的 kubeconfig 自动保存到 ~/.kube/config 文件

#### 04、安装docker服务

配置文件如下：

```shell
roles/docker/
├── files
│   ├── daemon.json
│   ├── docker
│   └── docker-tag
├── tasks
│   └── main.yml
└── templates
    └── docker.service.j2
```

##### 1、创建docker的service文件

```shel
[Unit]
Description=Docker Application Container Engine
Documentation=http://docs.docker.io

[Service]
Environment="PATH={{ bin_dir }}:/bin:/sbin:/usr/bin:/usr/sbin"
ExecStart={{ bin_dir }}/dockerd --log-level=error
ExecStartPost=/sbin/iptables -I FORWARD -s 0.0.0.0/0 -j ACCEPT
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure
RestartSec=5
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
Delegate=yes
KillMode=process

[Install]
WantedBy=multi-user.target
```

##### 2、配置国内镜像加速

```shell
{
  "registry-mirrors": ["https://registry.docker-cn.com"],
  "max-concurrent-downloads": 6
}
```

##### 3、清理iptables

```shell
iptables -F && iptables -X \
        && iptables -F -t nat && iptables -X -t nat \
        && iptables -F -t raw && iptables -X -t raw \
        && iptables -F -t mangle && iptables -X -t mangle
```

##### 4、验证docker

```shell
systemctl status docker # 服务状态
journalctl -u docker # 运行日志
docker version
docker info
```

`iptables-save|grep FORWARD` 查看 iptables filter表 FORWARD链，最后要有一个 `-A FORWARD -j ACCEPT` 保底允许规则 

```shell
iptables-save|grep FORWARD
:FORWARD ACCEPT [0:0]
:FORWARD DROP [0:0]
-A FORWARD -j DOCKER-USER
-A FORWARD -j DOCKER-ISOLATION
-A FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -o docker0 -j DOCKER
-A FORWARD -i docker0 ! -o docker0 -j ACCEPT
-A FORWARD -i docker0 -o docker0 -j ACCEPT
-A FORWARD -j ACCEPT
```

#### 05、安装k8s-master节点

配置文件目录：

```shell
roles/kube-master/
├── tasks
│   └── main.yml
└── templates
    ├── basic-auth.csv.j2
    ├── kube-apiserver.service.j2
    ├── kube-controller-manager.service.j2
    ├── kubernetes-csr.json.j2
    ├── kube-scheduler.service.j2
    └── token.csv.j2
```

部署master节点包含三个组件`apiserver` `scheduler` `controller-manager`，其中 :

- apiserver提供集群管理的REST API接口，包括认证授权、数据校验以及集群状态变更等

  - 只有API Server才直接操作etcd
  - 其他模块通过API Server查询或修改数据
  - 提供其他模块之间的数据交互和通信的枢纽

- scheduler负责分配调度Pod到集群内的node节点

  - 监听kube-apiserver，查询还未分配Node的Pod
  - 根据调度策略为这些Pod分配节点

- controller-manager由一系列的控制器组成，它通过apiserver监控整个集群的状态，并确保集群处于预期的工作状态

  master节点的高可用主要就是实现apiserver组件的高可用，在之前部署lb节点时候已经配置haproxy对它进行负载均衡。

##### 1、创建 kubernetes 证书签名请求

```shell
{
  "CN": "kubernetes",
  "hosts": [
    "127.0.0.1",
    "{{ MASTER_IP }}",
    "{{ NODE_IP }}",
    "{{ CLUSTER_KUBERNETES_SVC_IP }}",
    "kubernetes",
    "kubernetes.default",
    "kubernetes.default.svc",
    "kubernetes.default.svc.cluster",
    "kubernetes.default.svc.cluster.local"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "HangZhou",
      "L": "XS",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
```

kubernetes 证书既是服务器证书，同时apiserver又作为客户端证书去访问etcd 集群；作为服务器证书需要设置hosts 指定使用该证书的IP 或域名列表，需要注意的是：

- 多主高可用集群需要把master VIP地址 {{ MASTER_IP }} 也添加进去
- kubectl get svc 将看到集群中由api-server 创建的默认服务 kubernetes，因此也要把 kubernetes 服务名和各个服务域名也添加进去

##### 2、创建token认证

```shell
{{ BOOTSTRAP_TOKEN }},kubelet-bootstrap,10001,"system:kubelet-bootstrap"
```

##### 3、创建apiserver服务文件

```shell
[Unit]
Description=Kubernetes API Service
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target
After=etcd.service

[Service]
EnvironmentFile=-/etc/kubernetes/config
EnvironmentFile=-/etc/kubernetes/apiserver
ExecStart={{ bin_dir }}/kube-apiserver \
	    $KUBE_LOGTOSTDERR \
	    $KUBE_LOG_LEVEL \
	    $KUBE_ETCD_SERVERS \
	    $KUBE_API_ADDRESS \
	    $KUBE_API_PORT \
	    $KUBELET_PORT \
	    $KUBE_ALLOW_PRIV \
	    $KUBE_SERVICE_ADDRESSES \
	    $KUBE_ADMISSION_CONTROL \
	    $KUBE_API_ARGS
Restart=on-failure
Type=notify
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

**创建apiserver config配置文件**

```shell
#
## The address on the local server to listen to.
#KUBE_API_ADDRESS="--insecure-bind-address=sz-pg-oam-docker-test-001.tendcloud.com"
KUBE_API_ADDRESS="--advertise-address=172.16.5.121 --bind-address={{ NODE_IP }} --insecure-bind-address=127.0.0.1"
#
## The port on the local server to listen on.
#KUBE_API_PORT="--port=8080"
#
## Port minions listen on
#KUBELET_PORT="--kubelet-port=10250"
#
## Comma separated list of nodes in the etcd cluster
KUBE_ETCD_SERVERS="--etcd-servers={{ ETCD_ENDPOINTS }}"
#
## Address range to use for services
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range={{ SERVICE_CIDR }}"
#
## default admission control policies
KUBE_ADMISSION_CONTROL="--admission-control=ServiceAccount,NamespaceLifecycle,NamespaceExists,LimitRanger,ResourceQuota"
#
## Add your own!
KUBE_API_ARGS="--authorization-mode=Node,RBAC --runtime-config=rbac.authorization.k8s.io/v1beta1 --kubelet-https=true --anonymous-auth=false --token-auth-file={{ ca_dir }}/token.csv --service-node-port-range={{ NODE_PORT_RANGE }} --tls-cert-file={{ ca_dir }}/kubernetes.pem --tls-private-key-file={{ ca_dir }}//kubernetes-key.pem --client-ca-file=/etc/kubernetes/ssl/ca.pem --service-account-key-file={{ ca_dir }}/ca-key.pem --etcd-cafile={{ ca_dir }}//ca.pem --etcd-certfile={{ etcd_dir }}//etcd.pem --etcd-keyfile={{ etcd_dir }}/etcd-key.pem --enable-swagger-ui=true --allow-privileged=true --apiserver-count=3 --audit-log-maxage=30 --audit-log-maxbackup=3 --audit-log-maxsize=100 --audit-log-path=/var/lib/audit.log --event-ttl=1h"
```

##### 4、创建controller-manager 的服务文件

```shell
[Unit]
Description=Kube-controller-manager Service
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target
After=kube-apiserver.service
Requires=kube-apiserver.service
[Service]
Type=simple
EnvironmentFile=-/etc/kubernetes/config
EnvironmentFile=-/etc/kubernetes/controller-manager
ExecStart={{ bin_dir }}}kube-controller-manager \
        $KUBE_LOGTOSTDERR \
        $KUBE_LOG_LEVEL \
        $KUBE_MASTER \
        $KUBE_CONTROLLER_MANAGER_ARGS
Restart=always
LimitNOFILE=65536

[Install]
WantedBy=default.target
```

**创建controller-manager配置文件**

```shell
###
# The following values are used to configure the kubernetes controller-manager

# defaults from config and apiserver should be adequate

# Add your own!
KUBE_CONTROLLER_MANAGER_ARGS="--master=http://127.0.0.1:8080 --bind-address=127.0.0.1 --service-cluster-ip-range={{ SERVICE_CIDR }} --cluster-name=kubernetes --cluster-signing-cert-file={{ ca_dir }}/ca.pem --cluster-signing-key-file={{ ca_dir }}/ca-key.pem  --service-account-private-key-file={{ ca_dir }}/ca-key.pem --root-ca-file={{ ca_dir }}/ca.pem --leader-elect=true --cluster-cidr={{ CLUSTER_CIDR }} --node-monitor-grace-period=90s"
```

- --address 值必须为 127.0.0.1，因为当前 kube-apiserver 期望 scheduler 和 controller-manager 在同一台机器
- --master=[http://127.0.0.1:8080](http://127.0.0.1:8080/) 使用非安全 8080 端口与 kube-apiserver 通信
- --cluster-cidr 指定 Cluster 中 Pod 的 CIDR 范围，该网段在各 Node 间必须路由可达(calico 实现)
- --service-cluster-ip-range 参数指定 Cluster 中 Service 的CIDR范围，必须和 kube-apiserver 中的参数一致
- --cluster-signing-* 指定的证书和私钥文件用来签名为 TLS BootStrap 创建的证书和私钥
- --root-ca-file 用来对 kube-apiserver 证书进行校验，指定该参数后，才会在Pod 容器的 ServiceAccount 中放置该 CA 证书文件
- --leader-elect=true 使用多节点选主的方式选择主节点。只有主节点才会启动所有控制器，而其他从节点则仅执行选主算法

##### 5、创建scheduler服务文件

```shell
[Unit]
Description=Kubernetes Scheduler Plugin
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
EnvironmentFile=-/etc/kubernetes/config
EnvironmentFile=-/etc/kubernetes/scheduler
ExecStart={{ bin_dir }}/kube-scheduler \
	    $KUBE_LOGTOSTDERR \
	    $KUBE_LOG_LEVEL \
	    $KUBE_MASTER \
	    $KUBE_SCHEDULER_ARGS
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

**创建scheduler配置文件**

```shell
###
# kubernetes scheduler config

# default config should be adequate

# Add your own!
KUBE_SCHEDULER_ARGS="--master=http://127.0.0.1:8080 --leader-elect=true --address=127.0.0.1"
```

- --address 同样值必须为 127.0.0.1
- --master=[http://127.0.0.1:8080](http://127.0.0.1:8080/) 使用非安全 8080 端口与 kube-apiserver 通信
- --leader-elect=true 部署多台机器组成的 master 集群时选举产生一个处于工作状态的 kube-controller-manager 进程

##### 6、创建config配置文件

```shell
###
# kubernetes system config
#
# The following values are used to configure various aspects of all
# kubernetes services, including
#
#   kube-apiserver.service
#   kube-controller-manager.service
#   kube-scheduler.service
#   kubelet.service
#   kube-proxy.service
# logging to stderr means we get it in the systemd journal
KUBE_LOGTOSTDERR="--logtostderr=true"

# journal message level, 0 is debug
KUBE_LOG_LEVEL="--v=0"

# Should this cluster be allowed to run privileged docker containers
KUBE_ALLOW_PRIV="--allow-privileged=true"

# How the controller-manager, scheduler, and proxy find the apiserver
#KUBE_MASTER="--master=http://sz-pg-oam-docker-test-001.tendcloud.com:8080"
KUBE_MASTER="--master=http://127.0.0.1:8080"
```

##### 7、msater集群验证

```shell
# 查看进程状态
systemctl status kube-apiserver
systemctl status kube-controller-manager
systemctl status kube-scheduler
# 查看进程运行日志
journalctl -u kube-apiserver
journalctl -u kube-controller-manager
journalctl -u kube-scheduler
# 执行 kubectl get componentstatus 可以看到
NAME                 STATUS    MESSAGE              ERROR
scheduler            Healthy   ok                   
controller-manager   Healthy   ok                   
etcd-0               Healthy   {"health": "true"}   
```

#### 06、安装k8s-node节点

`kube-node` 是集群中承载应用的节点，前置条件需要先部署好`kube-master`节点(因为需要操作`用户角色绑定`、`批准kubelet TLS 证书请求`等)，它需要部署如下组件： 

- docker：运行容器
- calico： 配置容器网络 (或者 flannel)
- kubelet： kube-node上最主要的组件
- kube-proxy： 发布应用服务与负载均衡

配置文件目录如下：

```shell
roles/kube-node
├── tasks
│   └── main.yml
└── templates
    ├── cni-default.conf.j2
    ├── kubelet.service.j2
    ├── kube-proxy-csr.json.j2
    └── kube-proxy.service.j2
```

##### 1、创建角色绑定

kubelet 启动时向 kube-apiserver 发送 TLS bootstrapping 请求，需要先将 bootstrap token 文件中的 kubelet-bootstrap 用户赋予 system:node-bootstrapper 角色，然后 kubelet 才有权限创建认证请求 

```shell
# 增加15秒延时是为了等待上一步kube-master 启动完全
"sleep 15 && {{ bin_dir }}/kubectl create clusterrolebinding kubelet-bootstrap \
        --clusterrole=system:node-bootstrapper --user=kubelet-bootstrap"
```

##### 2、创建 bootstrapping kubeconfig 文件

```shell
#设置集群参数
  shell: "{{ bin_dir }}/kubectl config set-cluster kubernetes \
        --certificate-authority={{ ca_dir }}/ca.pem \
        --embed-certs=true \
        --server={{ KUBE_APISERVER }} \
        --kubeconfig=bootstrap.kubeconfig"
#设置客户端认证参数
  shell: "{{ bin_dir }}/kubectl config set-credentials kubelet-bootstrap \
        --token={{ BOOTSTRAP_TOKEN }} \
        --kubeconfig=bootstrap.kubeconfig"
#设置上下文参数
  shell: "{{ bin_dir }}/kubectl config set-context default \
        --cluster=kubernetes \
        --user=kubelet-bootstrap \
        --kubeconfig=bootstrap.kubeconfig"
#选择默认上下文
  shell: "{{ bin_dir }}/kubectl config use-context default --kubeconfig=bootstrap.kubeconfig"
```

- 注意 kubelet bootstrapping认证时是靠 token的，后续由 `master`为其生成证书和私钥
- 以上生成的bootstrap.kubeconfig配置文件需要移动到/etc/kubernetes/目录下，后续在kubelet启动参数中指定该目录下的 bootstrap.kubeconfig

##### 3、创建 kubelet 的服务文件

创建kubelet工作目录：/var/lib/kubelet

```shell
[Unit]
Description=Kubernetes Kubelet Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=docker.service
Requires=docker.service

[Service]
WorkingDirectory=/var/lib/kubelet
EnvironmentFile=-/etc/kubernetes/config
EnvironmentFile=-/etc/kubernetes/kubelet
ExecStart={{ bin_dir }}kubelet \
	    $KUBE_LOGTOSTDERR \
	    $KUBE_LOG_LEVEL \
	    $KUBELET_API_SERVER \
	    $KUBELET_ADDRESS \
	    $KUBELET_PORT \
	    $KUBELET_HOSTNAME \
	    $KUBE_ALLOW_PRIV \
	    $KUBELET_POD_INFRA_CONTAINER \
	    $KUBELET_ARG
#ExecStartPost=/sbin/iptables -A INPUT -s 10.0.0.0/8 -p tcp --dport 4194 -j ACCEPT
#ExecStartPost=/sbin/iptables -A INPUT -s 172.16.0.0/12 -p tcp --dport 4194 -j ACCEPT
#ExecStartPost=/sbin/iptables -A INPUT -s 192.168.0.0/16 -p tcp --dport 4194 -j ACCEPT
#ExecStartPost=/sbin/iptables -A INPUT -p tcp --dport 4194 -j DROP
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**创建kubelet配置文件**

```shell
###
## kubernetes kubelet (minion) config
#
## The address for the info server to serve on (set to 0.0.0.0 or "" for all interfaces)
#KUBELET_ADDRESS="--address=172.16.5.121"
#
## The port for the info server to serve on
#KUBELET_PORT="--port=10250"
#
## You may leave this blank to use the actual hostname
KUBELET_HOSTNAME="--hostname-override={{ NODE_IP }}"
#
## location of the api-server
## COMMENT THIS ON KUBERNETES 1.8+
# KUBELET_API_SERVER="--api-servers=http://172.20.0.113:8080"
KUBELET_CONFIG="--kubeconfig=/etc/kubernetes/kubelet.kubeconfig"
#
## pod infrastructure container
KUBELET_POD_INFRA_CONTAINER="--pod-infra-container-image={{ POD_INFRA_CONTAINER_IMAGE }}"
#
## Add your own!
KUBELET_ARGS=" --cluster-dns={{ CLUSTER_DNS_SVC_IP }} --serialize-image-pulls=false --image-gc-high-threshold=80 --image-gc-low-threshold=50 --bootstrap-kubeconfig=/etc/kubernetes/bootstrap.kubeconfig --kubeconfig=/etc/kubernetes/kubelet.kubeconfig --cert-dir={{ ca_dir }} --cluster-domain={{ CLUSTER_DNS_DOMAIN }} --hairpin-mode promiscuous-bridge --network-plugin=cni"
```

##### 3、批准kubelet 的 TLS 证书请求

```shell
sleep 15 && {{ bin_dir }}/kubectl get csr|grep 'Pending' | awk 'NR>0{print $1}'| xargs {{ bin_dir }}/kubectl certificate approve
```

- 增加15秒延时等待kubelet启动
- `kubectl get csr |grep 'Pending'` 找出待批准的 TLS请求
- `kubectl certificate approve` 批准请求

##### 4、创建kube-proxy证书请求

````shell
{
  "CN": "system:kube-proxy",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "GuangDong",
      "L": "ShenZhen",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
````

- CN 指定该证书的 User 为 system:kube-proxy，预定义的 ClusterRoleBinding system:node-proxier 将User system:kube-proxy 与 Role system:node-proxier 绑定，授予了调用 kube-apiserver Proxy 相关 API 的权限；
- kube-proxy 使用客户端证书可以不指定hosts 字段

##### 5、创建 kube-proxy kubeconfig 文件

```shell
#设置集群参数
  shell: "{{ bin_dir }}/kubectl config set-cluster kubernetes \
        --certificate-authority={{ ca_dir }}/ca.pem \
        --embed-certs=true \
        --server={{ KUBE_APISERVER }} \
        --kubeconfig=kube-proxy.kubeconfig"
#设置客户端认证参数
  shell: "{{ bin_dir }}/kubectl config set-credentials kube-proxy \
        --client-certificate={{ ca_dir }}/kube-proxy.pem \
        --client-key={{ ca_dir }}/kube-proxy-key.pem \
        --embed-certs=true \
        --kubeconfig=kube-proxy.kubeconfig"
#设置上下文参数
  shell: "{{ bin_dir }}/kubectl config set-context default \
        --cluster=kubernetes \
        --user=kube-proxy \
        --kubeconfig=kube-proxy.kubeconfig"
#选择默认上下文
  shell: "{{ bin_dir }}/kubectl config use-context default --kubeconfig=kube-proxy.kubeconfig"
```

- 生成的kube-proxy.kubeconfig 配置文件需要移动到/etc/kubernetes/目录，后续kube-proxy服务启动参数里面需要指定

##### 6、创建 kube-proxy服务文件

```shell
[Unit]
Description=Kubernetes Kube-Proxy Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
EnvironmentFile=-/etc/kubernetes/config
EnvironmentFile=-/etc/kubernetes/proxy
ExecStart=/usr/bin/kube-proxy \
	    $KUBE_LOGTOSTDERR \
	    $KUBE_LOG_LEVEL \
	    $KUBE_MASTER \
	    $KUBE_PROXY_ARGS
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

**创建kube-proxy配置文件**

```shell
###
# kubernetes proxy config

# default config should be adequate

# Add your own!
KUBE_PROXY_ARGS="--bind-address={{ NODE_IP }}  --hostname-override={{ NODE_IP }} \
 --hostname-override=  --hostname-override={{ NODE_IP }} \
 --kubeconfig=/etc/kubernetes/kube-proxy.kubeconfig"
```

- --hostname-override 参数值必须与 kubelet 的值一致，否则 kube-proxy 启动后会找不到该 Node，从而不会创建任何 iptables 规则
- 特别注意：kube-proxy 根据 --cluster-cidr 判断集群内部和外部流量，指定 --cluster-cidr 或 --masquerade-all 选项后 kube-proxy 才会对访问 Service IP 的请求做 SNAT；但是这个特性与calico 实现 network policy冲突，所以如果要用 network policy，这两个选项都不要指定.

##### 7、验证node

```shell
systemctl status kubelet	# 查看状态
systemctl status kube-proxy
journalctl -u kubelet		# 查看日志
journalctl -u kube-proxy 
# 运行 kubectl get node 可以看到类似
NAME            STATUS    ROLES     AGE       VERSION
192.168.174.10  Ready     <none>    2d        v1.12.5
192.168.174.11  Ready     <none>    2d        v1.12.5
```

#### 07、安装calico组件

K8S网络设计原则，在配置集群网络插件或者实践K8S 应用/服务部署请时刻想到这些原则 ：

- 1.每个Pod都拥有一个独立IP地址，Pod内所有容器共享一个网络命名空间
- 2.集群内所有Pod都在一个直接连通的扁平网络中，可通过IP直接访问
  - 所有容器之间无需NAT就可以直接互相访问
  - 所有Node和所有容器之间无需NAT就可以直接互相访问
  - 容器自己看到的IP跟其他容器看到的一样
- 3.Service cluster IP尽可在集群内部访问，外部请求需要通过NodePort、LoadBalance或者Ingress来访问

Kubernetes Pod的网络是这样创建的 ：

- 0.每个Pod除了创建时指定的容器外，都有一个kubelet启动时指定的`基础容器`，比如：`mirrorgooglecontainers/pause-amd64` `registry.access.redhat.com/rhel7/pod-infrastructure`
- 1.首先 kubelet创建`基础容器`生成network namespace
- 2.然后 kubelet调用网络CNI driver，由它根据配置调用具体的CNI 插件
- 3.然后 CNI 插件给`基础容器`配置网络
- 4.最后 Pod 中其他的容器共享使用`基础容器`的网络

配置文件目录如下：

```shell
roles/calico/
├── tasks
│   └── main.yml
└── templates
    ├── calico-csr.json.j2
    ├── calicoctl.cfg.j2
    ├── calico-rbac.yaml.j2
    └── calico.yaml.j2
```

##### 1、创建calico证书申请

```
{
  "CN": "calico",
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "GuangDong",
      "L": "ShenZhen",
      "O": "k8s",
      "OU": "System"
    }
  ]
}
```

- calico 使用客户端证书，所以hosts字段可以为空；后续可以看到calico证书用在四个地方：
  - calico/node 这个docker 容器运行时访问 etcd 使用证书
  - cni 配置文件中，cni 插件需要访问 etcd 使用证书
  - calicoctl 操作集群网络时访问 etcd 使用证书
  - calico/kube-controllers 同步集群网络策略时访问 etcd 使用证书

##### 2、创建 calico DaemonSet yaml文件和rbac 文件

- 详细配置参数请参考[calico官方文档](https://docs.projectcalico.org/v2.6/reference/node/configuration)
- calico-node是以docker容器运行在host上的，因此需要把之前的证书目录 /etc/calico/ssl挂载到容器中
- 配置ETCD_ENDPOINTS 、CA、证书等，所有{{ }}变量与ansible hosts文件中设置对应
- 配置集群POD网络 CALICO_IPV4POOL_CIDR={{ CLUSTER_CIDR }}
- **重要**本K8S集群运行在同网段kvm虚机上，虚机间没有网络ACL限制，因此可以设置`CALICO_IPV4POOL_IPIP=off`，如果你的主机位于不同网段，或者运行在公有云上需要打开这个选项 `CALICO_IPV4POOL_IPIP=always`
- 配置FELIX_DEFAULTENDPOINTTOHOSTACTION=ACCEPT 默认允许Pod到Node的网络流量，更多[felix配置选项](https://docs.projectcalico.org/v2.6/reference/felix/configuration)

##### 3、安装calico 网络

- 安装之前必须确保`kube-master`和`kube-node`节点已经成功部署
- 只需要在任意装有kubectl客户端的节点运行 `kubectl create `安装即可，脚本中选取`NODE_ID=node1`节点安装
- 等待15s后(视网络拉取calico相关镜像速度)，calico 网络插件安装完成，删除之前kube-node安装时默认cni网络配置

##### 4、配置calicoctl工具 [calicoctl.cfg.j2](https://github.com/gitplyx/kubeasz/blob/master/docs/roles/calico/templates/calicoctl.cfg.j2)

```shell
apiVersion: v1
kind: calicoApiConfig
metadata:
spec:
  datastoreType: "etcdv2"
  etcdEndpoints: {{ ETCD_ENDPOINTS }}
  etcdKeyFile: /etc/calico/ssl/calico-key.pem
  etcdCertFile: /etc/calico/ssl/calico.pem
  etcdCACertFile: /etc/calico/ssl/ca.pem
```

##### 5、验证calico网络

执行calico安装成功后可以验证如下：(需要等待镜像下载完成，有时候即便上一步已经配置了docker国内加速，还是可能比较慢，请确认以下容器运行起来以后，再执行后续验证步骤) 

```shell
kubectl get pod --all-namespaces
NAMESPACE     NAME                                       READY     STATUS    RESTARTS   AGE
kube-system   calico-kube-controllers-5c6b98d9df-xj2n4   1/1       Running   0          1m
kube-system   calico-node-4hr52                          2/2       Running   0          1m
kube-system   calico-node-8ctc2                          2/2       Running   0          1m
kube-system   calico-node-9t8md                          2/2       Running   0          1m
#查看网卡和路由信息
kubectl run test --image=busybox --replicas=3 sleep 30000
# 查看网卡信息
ip a
# 查看路由
route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    0      0        0 ens3
192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 ens3
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
172.20.3.64     192.168.1.34    255.255.255.192 UG    0      0        0 ens3
172.20.33.128   0.0.0.0         255.255.255.192 U     0      0        0 *
172.20.33.129   0.0.0.0         255.255.255.255 UH    0      0        0 caliccc295a6d4f
172.20.104.0    192.168.1.35    255.255.255.192 UG    0      0        0 ens3
172.20.166.128  192.168.1.63    255.255.255.192 UG    0      0        0 ens3
#查看所有calico节点状态
calicoctl node status
Calico process is running.

IPv4 BGP status
+--------------+-------------------+-------+----------+-------------+
| PEER ADDRESS |     PEER TYPE     | STATE |  SINCE   |    INFO     |
+--------------+-------------------+-------+----------+-------------+
| 192.168.1.34 | node-to-node mesh | up    | 12:34:00 | Established |
| 192.168.1.35 | node-to-node mesh | up    | 12:34:00 | Established |
| 192.168.1.63 | node-to-node mesh | up    | 12:34:01 | Established |
+--------------+-------------------+-------+----------+-------------+
BGP 协议是通过TCP 连接来建立邻居的，因此可以用netstat 命令验证 BGP Peer
netstat -antlp|grep ESTABLISHED|grep 179
tcp        0      0 192.168.1.66:179        192.168.1.35:41316      ESTABLISHED 28479/bird      
tcp        0      0 192.168.1.66:179        192.168.1.34:40243      ESTABLISHED 28479/bird      
tcp        0      0 192.168.1.66:179        192.168.1.63:48979      ESTABLISHED 28479/bird
# 查看集群ipPool情况
calicoctl get ipPool -o yaml
- apiVersion: v1
  kind: ipPool
  metadata:
    cidr: 172.20.0.0/16
  spec:
    nat-outgoing: true   
```

#### 08、集群管理

##### 1、安装主要组件

```shell
# 安装kubedns
kubectl create -f /etc/ansible/manifests/kubedns
# 安装heapster
kubectl create -f /etc/ansible/manifests/heapster
# 安装dashboard
kubectl create -f /etc/ansible/manifests/dashboard
```

更新后dashboard已经默认关闭非安全端口访问，请使用https://xx.xx.xx.xx:6443/api/v1/namespaces/kube-system/services/kubernetes-dashboard/proxy访问，并用默认用户 admin:test1234 登陆，更多内容请查阅dashboard













