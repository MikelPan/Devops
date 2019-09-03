### 安装kubeadm
k8s_version=1.15.2
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
yum install -y kubeadm-$k8s_version kubelet-$k8s_version kubectl-$k8s_version
systemctl enable kubelet && systemctl start kubelet