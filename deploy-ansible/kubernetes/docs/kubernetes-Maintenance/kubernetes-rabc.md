### 创建ServiceAccount
```shell
# 创建serviceaccount
kubectl create  serviceaccount  myaccount -o yaml --dry-run > myaccount.yaml
# 查看serviceaccount
kubectl get sa
```
### 创建secret
```shell
# 创建docker registry
kubectl create secret docker-registry seract-name \
  --docker-server=registry.fjhb.cn  \
  --docker-username=test \
  --docker-password=123 \
  --docker-email=ylw@fjhb.cn
# 生成docker registry
apiVersion: v1
kind: Secret
metadata:
  name: seract-name
  namespace: delopment
data:
    .dockerconfigjson: {base64 -w 0 ~/.docker/config.json}
type: kubernetes.io/dockerconfigjson
```

