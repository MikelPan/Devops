#### 入口手动配置trafix ssl 访问
**创建traefix cert**
```shell
kubectl create secret generic traefik-cert --from-file=tls.crt --from-file=tls.key -n kube-system
```
**创建trafix toml文件**
```shell
defaultEntryPoints = ["http","https"]
[entryPoints]
[entryPoints.http]
address = ":80"
[entryPoints.http.redirect]
entryPoint = "https"
[entryPoints.https]
address = ":443"
[entryPoints.https.tls]
  [[entryPoints.https.tls.certificates]]
  certFile = "/ssl/tls.crt"
  keyFile = "/ssl/tls.key"
```
**创建configmap文件**
```shell
kubectl create configmap traefik-conf --from-file=traefik.toml -n kube-system
```
**创建trafix-deployment文件**
```yaml

---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: traefik-ingress-controller
rules:
  - apiGroups:
      - ""
    resources:
      - services
      - endpoints
      - secrets
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - extensions
    resources:
      - ingresses
    verbs:
      - get
      - list
      - watch
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: traefik-ingress-controller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: traefik-ingress-controller
subjects:
- kind: ServiceAccount
  name: traefik-ingress-controller
  namespace: kube-system
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: traefik-ingress-controller
  namespace: kube-system
---
kind: DaemonSet
apiVersion: extensions/v1beta1
metadata:
  name: traefik-ingress-controller
  namespace: kube-system
  labels:
    k8s-app: traefik-ingress-lb
spec:
  selector:
    matchLabels:
      k8s-app: traefik-ingress-lb
  template:
    metadata:
      labels:
        k8s-app: traefik-ingress-lb
        name: traefik-ingress-lb
    spec:
      serviceAccountName: traefik-ingress-controller
      terminationGracePeriodSeconds: 60
      hostNetwork: true
      volumes:
      - name: ssl
        secret:
          secretName: traefik-cert
      - name: config
        configMap:
          name: traefik-conf
      containers:
      - image: traefik
        name: traefik-ingress-lb
        volumeMounts:
        - mountPath: "/etc/kubernetes/ssl/" #ssl路径
          name: "ssl"
        - mountPath: "/etc/k8s/conf/"  #conf路径
          name: "config"
        ports:
        - name: http
          containerPort: 80
        - name: https
          containerPort: 443
        - name: admin
          containerPort: 8080
        args:
        - --api
        - --kubernetes
        - --configfile=/etc/k8s/conf/traefik.toml
---
kind: Service
apiVersion: v1
metadata:
  name: traefik-ingress-service
  namespace: kube-system
spec:
  selector:
    k8s-app: traefik-ingress-lb
  ports:
    - protocol: TCP
      port: 80
      name: web
    - protocol: TCP
      port: 443
      name: https
    - protocol: TCP
      port: 8080
      name: admin
  type: NodePort
```
**创建ui 服务**
```yaml

---
apiVersion: v1
kind: Service
metadata:
  name: traefik-web-ui
  namespace: kube-system
spec:
  selector:
    k8s-app: traefik-ingress-lb
  ports:
  - name: web
    port: 80
    targetPort: 8080

---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: traefik-web-ui
  namespace: kube-system
  annotations:
    kubernetes.io/ingress.class: traefik
spec:
  tls:
    - secretName: traefik-cert #引用证书
  rules:
  - host: tf.abcgogo.com #自己的域名
    http:
      paths:
      - path: /
        backend:
          serviceName: traefik-web-ui
          servicePort: web
```
