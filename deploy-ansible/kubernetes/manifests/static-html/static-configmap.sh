kubectl delete configmap static-html-config -n kube-system
kubectl create configmap static-html-config --from-file=config-file=default.conf -n kube-system