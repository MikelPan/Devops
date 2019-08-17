### kubeadm 集群证书过期处理
#### 通过生成新证书替换
```shell
# 证书过期处理
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text |grep ' Not '
# 备份证书
mkdir /etc/kubernetes/{pki_back,conf_back}
cd /etc/kubernetes
mv pki/apiserver* ./pki_bak/
mv pki/front-proxy-client.* ./pki_bak/
mv ./admin.conf ./conf_bak/
mv ./kubelet.conf ./conf_bak/
mv ./controller-manager.conf ./conf_bak/
mv ./scheduler.conf ./conf_bak/

## 编译源代码方式
# 创建证书
kubeadm alpha phase certs all --config  ~/kubeadm.yaml
# 生成新配置文件
kubeadm alpha phase kubeconfig all --config ~/kubeadm.yaml
# 替换证书
for crt in $(find /etc/kubernetes/pki/ -name "*.crt"); do openssl x509 -in $crt -noout -dates; done

## 手动创建证书
# 创建证书
kubeadm alpha phase certs all --apiserver-advertise-address=${MASTER_API_SERVER_IP} --apiserver-cert-extra-sans=主机内网ip,主机公网ip

# 生成新配置文件
kubeadm alpha phase kubeconfig all --apiserver-advertise-address=${MASTER_API_SERVER_IP}

# 将新生成的admin配置文件覆盖掉原本的admin文件
mv $HOME/.kube/config $HOME/.kube/config.old
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
sudo chmod 777 $HOME/.kube/config
```
#### 通过配置自动轮转
```
# 在/etc/systemd/system/kubelet.service.d/10-kubeadm.conf 增加如下参数
Environment="KUBELET_EXTRA_ARGS=--feature-gates=RotateKubeletServerCertificate=true"
# 在/etc/kubernetes/manifests/kube-controller-manager.yaml 添加如下参数
  - command:
    - kube-controller-manager
    - --experimental-cluster-signing-duration=87600h0m0s
    - --feature-gates=RotateKubeletServerCertificate=true
# 创建证书更新文件
cat > ca-update.yaml << EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: system:certificates.k8s.io:certificatesigningrequests:selfnodeserver
rules:
- apiGroups:
  - certificates.k8s.io
  resources:
  - certificatesigningrequests/selfnodeserver
  verbs:
  - create
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kubeadm:node-autoapprove-certificate-server
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:certificates.k8s.io:certificatesigningrequests:selfnodeserver
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:nodes
EOF
kubectl create –f ca-update.yaml
# 重启