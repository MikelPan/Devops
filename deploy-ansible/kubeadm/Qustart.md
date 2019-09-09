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
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "data-root":"/var/lib/docker",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ],
  "insecure-registries": [],
  "registry-mirrors": ["https://uyah70su.mirror.aliyuncs.com"]
}}
EOF
```
##### ubuntu安装
```shell
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get -y update
sudo apt-get -y install docker-ce
```
##### 安装kubeadm
```shell
# 下载离线包
yum install -y wget
wget -c https://sealyun.oss-cn-beijing.aliyuncs.com/free/kube1.15.0.tar.gz
wget -c https://github.com/fanux/sealos/releases/download/v2.0.4/sealos
chmod +x sealos && cp sealos /usr/bin
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
sealos init --master 192.168.248.134 \
    --node 192.168.248.135 \                 
    --user root \                        
    --passwd 123456 \      
    --version v1.15.0 \
    --pkg-url /root/kube1.15.0.tar.gz 
# 清理集群
sealos clean \
    --master 192.168.174.134 \
    --node 192.168.174.135 \
    --user root \
    --passwd 123456
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
# 使用自定义配置安装集群
sealos config -t kubeadm >>  kubeadm-config.yaml.tmpl
sealos init --kubeadm-config kubeadm-config.yaml.tmpl \
    --master 192.168.0.2 \
    --master 192.168.0.3 \
    --master 192.168.0.4 \
    --node 192.168.0.5 \
    --user root \
    --passwd your-server-password \
    --version v1.14.1 \
    --pkg-url /root/kube1.14.1.tar.gz 
# 增加节点
## 通过kubeadm
kubeadm token create --print-join-command
echo "10.103.97.2 apiserver.cluster.local" >> /etc/hosts   # using vip
kubeadm join 10.103.97.2:6443 --token 9vr73a.a8uxyaju799qwdjv \
    --master 10.103.97.100:6443 \
    --master 10.103.97.101:6443 \
    --master 10.103.97.102:6443 \
    --discovery-token-ca-cert-hash sha256:7c2e69131a36ae2a042a339b33381c6d0d43887e2de83720eff5359e26aec866
## 通过sealos
sealos join 
    --master 192.168.0.2 \
    --master 192.168.0.3 \
    --master 192.168.0.4 \
    --vip 10.103.97.2 \       
    --node 192.168.0.5 \            
    --user root \             
    --passwd your-server-password \
    --pkg-url /root/kube1.15.0.tar.gz 
## 手动指定使用kubeadm安装
cat > kubeadm-config.yaml.tmp <<EOF
apiVersion: kubeadm.k8s.io/v1beta2
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
  advertiseAddress: 172.18.13.234 
  bindPort: 6443
nodeRegistration:
  criSocket: /var/run/dockershim.sock
  name: k8s-master01
  taints:
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
---
apiServer:
  certSANs:
  - 172.18.12.14
  - 127.0.0.1
  - apiserver.cluster.local
  extraArgs:
    authorization-mode: Node,RBAC
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta2
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controllerManager: {}
dns:
  type: CoreDNS
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: registry.aliyuncs.com/google_containers
kind: ClusterConfiguration
kubernetesVersion: v1.15.2
controlPlaneEndpoint: "apiserver.cluster.local:6443"
networking:
  dnsDomain: cluster.local
  podSubnet: 10.0.0.0/16
  serviceSubnet: 10.96.0.0/12
scheduler: {}
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
featureGates:
  SupportIPVSProxyMode: true
mode: ipvs
EOF
cat > kubeadm-config.yaml <<EOF
apiVersion: kubeadm.k8s.io/v1beta1
kind: ClusterConfiguration
kubernetesVersion: v1.14.0
controlPlaneEndpoint: "apiserver.cluster.local:6443" # apiserver DNS name
apiServer:
        certSANs:
        - 127.0.0.1
        - apiserver.cluster.local
        - 172.20.241.205
        - 172.20.241.206
        - 172.20.241.207
        - 172.20.241.208
        - 10.103.97.1          # virturl ip
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
ipvs:
        excludeCIDRs: 
        - "10.103.97.1/32" # 注意不加这个kube-proxy会清理你的规则
EOF
### 安装msater0
echo "10.103.97.100 apiserver.cluster.local" >> /etc/hosts # 解析的是master0的地址
kubeadm init --config=kubeadm-config.yaml --experimental-upload-certs  
mkdir ~/.kube && cp /etc/kubernetes/admin.conf ~/.kube/config
kubectl apply -f https://docs.projectcalico.org/v3.6/getting-started/kubernetes/installation/hosted/kubernetes-datastore/calico-networking/1.7/calico.yaml
### 安装master1
echo "10.103.97.101 apiserver.cluster.local" >> /etc/hosts #解析的是master0的地址,为了能正常join进去
kubeadm join 10.103.97.101:6443 --token 9vr73a.a8uxyaju799qwdjv \
    --discovery-token-ca-cert-hash sha256:7c2e69131a36ae2a042a339b33381c6d0d43887e2de83720eff5359e26aec866 \
    --experimental-control-plane \
    --certificate-key f8902e114ef118304e561c3ecd4d0b543adc226b7a07f675f56564185ffe0c07
### 安装master2
echo "10.103.97.100 apiserver.cluster.local" >> /etc/hosts
kubeadm join 10.103.97.102:6443 --token 9vr73a.a8uxyaju799qwdjv \
    --discovery-token-ca-cert-hash sha256:7c2e69131a36ae2a042a339b33381c6d0d43887e2de83720eff5359e26aec866 \
    --experimental-control-plane \
    --certificate-key f8902e114ef118304e561c3ecd4d0b543adc226b7a07f675f56564185ffe0c07
### 安装node节点
echo "10.103.97.1 apiserver.cluster.local" >> /etc/hosts   # 需要解析成虚拟ip
kubeadm join 10.103.97.1:6443 --token 9vr73a.a8uxyaju799qwdjv \
    --master 10.103.97.100:6443 \
    --master 10.103.97.101:6443 \
    --master 10.103.97.102:6443 \
    --discovery-token-ca-cert-hash sha256:7c2e69131a36ae2a042a339b33381c6d0d43887e2de83720eff5359e26aec866
## 版本升级
### 升级master
kubeadm upgrade plan
kubeadm upgrade apply v1.15.0
systemctl restart kubelet  # 拷贝kubelet二进制文件到/usr/bin
kubeadm upgrade apply  # 升级其他控制节点
### 升级node节点
kubectl drain $NODE --ignore-daemonsets  # 驱逐节点
kubeadm upgrade node config --kubelet-version v1.15.0
systemctl restart kubelet   # 拷贝kubelet二进制文件到/usr/bin
kubectl uncordon $NODE      # 重新调度
```