### 安装nfs服务器
```shell
# 安装nfs
yum install -y nfs-utils
systemctl enable rpcbind
systemctl enable nfs
systemctl start rpcbind
systemctl start nfs
# 创建共享目录
mkdir /nfs
cat > /etc/exports <<EOF
/nfs *(rw,sync,insecure,no_subtree_check,no_root_squash)
EOF
# 启动nfs
systemctl start rpcbind
systemctl start nfs
```
### 安装动态卷
```shell
# 安装动态卷
kubectl apply -f  nfs-provileges.yaml
```