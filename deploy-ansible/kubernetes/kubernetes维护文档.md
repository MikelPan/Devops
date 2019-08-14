#### 查看etcd 中flanal信息
```shell
>>>>>>> 16ebcf3581b7fa80ba295abd20f913276d4b5b1f
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
  
#### pv temring无法删除
```shell
kubectl patch pvc pvc_name -p '{"metadata":{"finalizers":null}}'
```

#### helm的使用
##### 安装helm

##### 创建char
```shell
helm create mychart
rm -rf mychart/templates/*.*
```
##### 创建模板
```shell
cat > mychart/templates/configmap.yaml <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{.Release.Name}}-configmap
data:
  myvalue: "Hello World"
EOF
```
#### 镜像拉取策略
```shell
imagePullPolicy: IfNotPresent
```

