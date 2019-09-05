<<<<<<< HEAD
#!/bin/bash
# 初始化kubeadm
kubeadm config print init-defaults > kubeadm-config.yaml
kubeadm init --config=kubeadm-config.yaml --experimental-upload-certs | tee kubeadm-init.log
cat << EOF >> ~/.bashrc
export KUBECONFIG=/etc/kubernetes/admin.conf
EOF
source ~/.bashrc
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# 安装flnanel
wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
cat kube-flannel.yml | grep image
cat kube-flannel.yml | grep 10.244
sed -i 's#quay.io/coreos/flannel:v0.11.0-amd64#willdockerhub/flannel:v0.11.0-amd64#g' kube-flannel.yml
kubectl apply -f kube-flannel.yml

# master节点允许调度
kubectl taint node k8s-master node-role.kubernetes.io/master-

# 其他master节点加入
kubeadm join 192.168.92.30:6444 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:c0a1021e5d63f509a0153724270985cdc22e46dc76e8e7b84d1fbb5e83566ea8 \
    --experimental-control-plane --certificate-key 52f64a834454c3043fe7a0940f928611b6970205459fa19cb1193b33a288e7cc

# 其他node节点加入
kubeadm join 192.168.92.30:6444 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:c0a1021e5d63f509a0153724270985cdc22e46dc76e8e7b84d1fbb5e83566ea8

# 查看node 标签
kuebctl get nodes --show-labels

# 给节点打上标签
for i in $(kubectl get nodes | awk '{print $1} | sed -n '2,$p')
    do
        kubectl label nodes $i node=$i
    done

=======
#!/bin/bash
# 初始化kubeadm
kubeadm config print init-defaults > kubeadm-config.yaml
kubeadm init --config=kubeadm-config.yaml --experimental-upload-certs | tee kubeadm-init.log
cat << EOF >> ~/.bashrc
export KUBECONFIG=/etc/kubernetes/admin.conf
EOF
source ~/.bashrc
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# 安装flnanel
wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
cat kube-flannel.yml | grep image
cat kube-flannel.yml | grep 10.244
sed -i 's#quay.io/coreos/flannel:v0.11.0-amd64#willdockerhub/flannel:v0.11.0-amd64#g' kube-flannel.yml
kubectl apply -f kube-flannel.yml

# master节点允许调度
kubectl taint node k8s-master node-role.kubernetes.io/master-

# 其他master节点加入
kubeadm join 192.168.92.30:6444 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:c0a1021e5d63f509a0153724270985cdc22e46dc76e8e7b84d1fbb5e83566ea8 \
    --experimental-control-plane --certificate-key 52f64a834454c3043fe7a0940f928611b6970205459fa19cb1193b33a288e7cc

# 其他node节点加入
kubeadm join 192.168.92.30:6444 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:c0a1021e5d63f509a0153724270985cdc22e46dc76e8e7b84d1fbb5e83566ea8

# 查看node 标签
kuebctl get nodes --show-labels

# 给节点打上标签
for i in $(kubectl get nodes | awk '{print $1} | sed -n '2,$p')
    do
        kubectl label nodes $i node=$i
    done
>>>>>>> 5d18a167ad22271aab540cd7bb2e5ed49895534e
