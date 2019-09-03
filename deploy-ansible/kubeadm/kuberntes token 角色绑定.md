#### kubernetes role 
使用ServiceAccount Token的方式访问集群
```shell
# 使用 admin ServiceAccount来获取token
kubectl get sa admin -n kube-system -o yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2019-07-18T10:56:25Z"
  labels:
    k8s-app: kubernetes-dashboard
  name: admin
  namespace: kube-system
  resourceVersion: "115522"
  selfLink: /api/v1/namespaces/kube-system/serviceaccounts/admin
  uid: ca3d322c-4d63-4097-9931-6da8a2570d13
secrets:
- name: admin-token-hfzjc
# 查看对应的clusterrolebinding：
kubectl get clusterrolebinding admin-user -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  creationTimestamp: "2019-07-18T10:57:23Z"
  name: admin-user
  resourceVersion: "115602"
  selfLink: /apis/rbac.authorization.k8s.io/v1/clusterrolebindings/admin-user
  uid: b7e70e28-f0cf-4926-9c68-b5ba9e44fa77
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
查看admin sa绑定的clusterrole和对应的权限
kubectl get clusterrole cluster-admin -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  creationTimestamp: "2019-07-17T11:18:47Z"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: cluster-admin
  resourceVersion: "43"
  selfLink: /apis/rbac.authorization.k8s.io/v1/clusterroles/cluster-admin
  uid: e6a9199c-ef31-4592-a706-6ef3e0cc69cc
rules:
- apiGroups:
  - '*'
  resources:
  - '*'
  verbs:
  - '*'
- nonResourceURLs:
  - '*'
  verbs:
  - '*'
# 获取对应sa的secret从中获取token,并进行base64解码
kubectl get secret admin-token-hfzjc -n kube-system -o jsonpath={".data.token"} | base64 -d

eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi1oZnpqYyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImNhM2QzMjJjLTRkNjMtNDA5Ny05OTMxLTZkYThhMjU3MGQxMyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTphZG1pbiJ9.YBcqIXPKfyfTiwxoW0XBzidflx6Ck4c4BQGtblkN21BhmhnK24NYAIZ8jtZ2F1FhLdx_SAfuLG9cBMMmbRSdSxmQ43DB2EQUB9mGBRIWo6kKRB0TfRwUBHfmaTUDCrWYUqcvBxgjbrzQTF5JWnMhzkH1uBVlZPui9Z6TyelOFstLUpRjIxYsIQuhIIwaANPzHd4s6WyrlhwdUBO1rAlcTFlyHhbknvNNJmyfCba8vowaluFJNDOjqxo5IcCyOOudXaxCYqsBFcywB38WA_5UXIQJwsIjR65YOENq6jhayw3emsE_LKNmhksCPQoka3rhEiMGidc9IpYVBsrjJLyG3Q

curl -k -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi1oZnpqYyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImNhM2QzMjJjLTRkNjMtNDA5Ny05OTMxLTZkYThhMjU3MGQxMyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTphZG1pbiJ9.YBcqIXPKfyfTiwxoW0XBzidflx6Ck4c4BQGtblkN21BhmhnK24NYAIZ8jtZ2F1FhLdx_SAfuLG9cBMMmbRSdSxmQ43DB2EQUB9mGBRIWo6kKRB0TfRwUBHfmaTUDCrWYUqcvBxgjbrzQTF5JWnMhzkH1uBVlZPui9Z6TyelOFstLUpRjIxYsIQuhIIwaANPzHd4s6WyrlhwdUBO1rAlcTFlyHhbknvNNJmyfCba8vowaluFJNDOjqxo5IcCyOOudXaxCYqsBFcywB38WA_5UXIQJwsIjR65YOENq6jhayw3emsE_LKNmhksCPQoka3rhEiMGidc9IpYVBsrjJLyG3Q' https://112.74.181.137:6443
```