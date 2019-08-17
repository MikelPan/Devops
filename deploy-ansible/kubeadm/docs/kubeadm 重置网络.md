### kubernetes 重置网络
#### 重置flannel
```shell
kubeadm reset
systemctl stop kubelet
systemctl stop docker
rm -rf /var/lib/cni/
rm -rf /var/lib/kubelet/*
rm -rf /etc/cni/
ifconfig cni0 down
ifconfig flannel.1 down
ifconfig docker0 down
ip link delete cni0
ip link delete flannel.1
systemctl start docker
```
#### 重置calico网络
```shell
kubeadm reset
systemctl stop kubelet
systemctl stop docker
rm -rf /var/lib/kubelet/*
rm -rf /etc/cni/
rm -rf /etc/calico/
rm -rf /var/run/calico/
rm -rf /var/lib/calico/
rm -rf /var/log/calico/
rm -rf /var/lib/cni/
ifconfig tunl0@NONE down
ifconfig docker0 down
ip link del cni0
ip link del dummy0
ip link del kube-ipvs0
```
#### 删除iptables规则
```shell
iptables -F && iptables -X \
&& iptables -F -t nat && iptables -X -t nat \
&& iptables -F -t raw && iptables -X -t raw \
&& iptables -F -t mangle && iptables -X -t mangle
```
