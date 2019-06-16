### 配置集群
#### 1、启动centos容器
```shell
# 启动配置redis集群的容器
kubectl run -i --tty centos-conf-redis --image=centos --restart=Never /bin/bash
# 配置容器
cat >> /etc/yum.repos.d/epel.repo<<'EOF'
[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
baseurl=https://mirrors.tuna.tsinghua.edu.cn/epel/7/$basearch
#mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-7&arch=$basearch
failovermethod=priority
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
EOF
# 安装软件
yum install -y epel-release
yum makecache fast
yum install -y vim wget redis-trib.noarch bind-utils
```
#### 2、集群初始化
```shell
# 创建一主一从的集群
redis-trib create --replicas 1 \
`dig +short redis-app-0.redis-service.development.svc.cluster.local`:6379 \
`dig +short redis-app-1.redis-service.default.svc.cluster.local`:6379 \
`dig +short redis-app-2.redis-service.default.svc.cluster.local`:6379 \
`dig +short redis-app-3.redis-service.default.svc.cluster.local`:6379 \
`dig +short redis-app-4.redis-service.default.svc.cluster.local`:6379 \
`dig +short redis-app-5.redis-service.default.svc.cluster.local`:6379
```

