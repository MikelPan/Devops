前言
Heketi
Heketi提供了一个RESTful管理界面，可以用来管理GlusterFS卷的生命周期。 通过Heketi，就可以像使用OpenStack Manila，Kubernetes和OpenShift一样申请可以动态配置GlusterFS卷。Heketi会动态在集群内选择bricks构建所需的volumes，这样以确保数据的副本会分散到集群不同的故障域内。同时Heketi还支持任意数量的ClusterFS集群，以保证接入的云服务器不局限于单个GlusterFS集群。
Gluster-Kubernetes
Gluster-Kubernetes是一个可以将GluserFS和Hekiti轻松部署到Kubernetes集群的开源项目。另外也提供在Kubernetes中可以采用StorageClass来动态管理GlusterFS卷
# 部署
```shell
# 下载
wget https://github.com/gluster/gluster-kubernetes/archive/v1.2.0.zip
unzip v1.2.0.zip
# 修改文件 topology.json.example
{
  "clusters": [
    {
      "nodes": [
        {
          "node": {
            "hostnames": {
              "manage": [
                "k8s-master01"
              ],
              "storage": [
                "172.18.28.157"
              ]
            },
            "zone": 1
          },
          "devices": [
            "/dev/mapper/data-glusterfslv",
          ]
        },
        {
          "node": {
            "hostnames": {
              "manage": [
                "k8s-master02"
              ],
              "storage": [
                "172.18.28.158"
              ]
            },
            "zone": 1
          },
          "devices": [
            "/dev/mapper/data-glusterfslv",
          ]
        },
        {
          "node": {
            "hostnames": {
              "manage": [
                "k8s-master03"
              ],
              "storage": [
                "172.18.28.159"
              ]
            },
            "zone": 1
          },
          "devices": [
            "/dev/mapper/data-glusterfslv",
          ]
        },
        {
          "node": {
            "hostnames": {
              "manage": [
                "k8s-node01"
              ],
              "storage": [
                "172.18.28.160"
              ]
            },
            "zone": 1
          },
          "devices": [
            "/dev/mapper/data-glusterfslv",
          ]
        },
      ]
    }
  ]
}
## 部署hekit
# 下载客户端
wget https://github.com/heketi/heketi/releases/download/v9.0.0/heketi-client-v9.0.0.linux.amd64.tar.gz
tar zxvf heketi-client-v9.0.0.linux.amd64.tar.gz -C /usr/local/src chmod +x /usr/local/src/heketi-cli && cp /usr/local/src/heketi-cli /usr/bin/
kubectl create ns heketi
# 手动加载模块 (节点上)
modprobe dm_thin_pool
lsmod  | grep thin
# 修改模板文件 添加
vim heketi-deployment.yaml deploy-heketi-deployment.yaml
type: LoadBalancer
# 删除标签
kubectl label node k8s-master01 storagenode-
kubectl label node k8s-master02 storagenode-
kubectl label node k8s-master03 storagenode-
kubectl label node k8s-master04 storagenode-
# 删除对应的pod
kubectl delete daemonset glusterfs -n heketi
kubectl delete deployment deploy-heketi -n heketi
# 安装过程中需要去掉注释 --show-all
./gk-deploy -g -c kubectl -t ./kube-templates -n heketi -l ./log.txt -v topology.json
# 手动加载模块
modprobe dm_thin_pool
lsmod  | grep thin
# 导出kekiserver
export HEKETI_CLI_SERVER=http://10.101.1.165:8080
# 查看拓扑信息
heketi-cli topology info
# 查看volume信息
heketi-cli volume list
heketi-cli volume info 9f08272aedc22b71abd71f2c2f6301d3
# 创建enpoints配置文件
heketi-cli volume create --size=200 \
--persistent-volume \
--persistent-volume-endpoint=heketi-storage-endpoints >heketi-storage-endpoints.yaml
# 创建enpoints
kubectl create -f heketi-storage-endpoints.yaml -n kube-system
# 查看enpoints
kubectl get endpoints -n kube-system
# 创建strogress class文件
vim gluster-storage-class.yaml
apiVersion: storage.k8s.io/v1beta1
kind: StorageClass
metadata:
  name: gluster-heketi
provisioner: kubernetes.io/glusterfs
parameters:
  resturl: "http://10.101.1.165:8080"
  restauthenabled: "flase"
  restuser: "admin"
  secretNamespace: "default"
  secretName: "heketi-secret"
# 创建pvc
vim gluster-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: glusterfs-claim
  annotations:
    volume.beta.kubernetes.io/storage-class: gluster-heketi
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
# 挂载pvc
vim app.yaml
apiVersion: v1
kind: Pod
metadata:
  name: busybox
spec:
  containers:
    - image: busybox
      command:
        - sleep
        - "3600"
      name: busybox
      volumeMounts:
        - mountPath: /usr/share/busybox
          name: mypvc
  volumes:
    - name: mypvc
      persistentVolumeClaim:
        claimName: glusterfs-claim
```