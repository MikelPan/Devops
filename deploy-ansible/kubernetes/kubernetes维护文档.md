#### k8s查看flananal的网络
```shell
https://10.113.184.66:2379,https://10.113.184.67:2379,https://10.113.184.68:2379
etcdctl --endpoints=https://10.113.184.66:2379,https://10.113.184.67:2379,https://10.113.184.68:2379 \
  --ca-file=/etc/kubernetes/ssl/ca.pem \
  --cert-file=/etc/kubernetes/ssl/kubernetes.pem \
  --key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
  ls /kube.runsdata.com/network/subnets
  
etcdctl --endpoints=https://10.113.184.66:2379,https://10.113.184.67:2379,https://10.113.184.68:2379 \
  --ca-file=/etc/kubernetes/ssl/ca.pem \
  --cert-file=/etc/kubernetes/ssl/kubernetes.pem \
  --key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
  get /kube.runsdata.com/network/config
    
etcdctl --endpoints=https://10.113.184.66:2379,https://10.113.184.67:2379,https://10.113.184.68:2379 \
  --ca-file=/etc/kubernetes/ssl/ca.pem \
  --cert-file=/etc/kubernetes/ssl/kubernetes.pem \
  --key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
  get /kube.runsdata.com/network/subnets/10.1.103.0-24
  
etcdctl --endpoints=https://10.113.184.66:2379,https://10.113.184.67:2379,https://10.113.184.68:2379 \
  --ca-file=/etc/kubernetes/ssl/ca.pem \
  --cert-file=/etc/kubernetes/ssl/kubernetes.pem \
  --key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
  ls /kube.runsdata.com/network
  
  
  etcdctl --endpoints=https://10.113.184.66:2379,https://10.113.184.67:2379,https://10.113.184.68:2379 \
  --ca-file=/etc/kubernetes/ssl/ca.pem \
  --cert-file=/etc/kubernetes/ssl/kubernetes.pem \
  --key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
  set /kube.runsdata.com/network/config '{"Network":"10.1.0.0/16","SubnetLen":24,"Backend":{"Type":"vxlan"}}'
```  
#### pv temring无法删除
```shell
kubectl patch pvc pvc_name -p '{"metadata":{"finalizers":null}}'
```

#### 指定调度
```shell
nodeSelector:
  server: server01
```
#### 镜像拉取策略
```shell
imagePullPolicy: IfNotPresent
```
