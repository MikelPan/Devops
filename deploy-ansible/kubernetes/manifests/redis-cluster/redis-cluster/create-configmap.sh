kubectl delete configmap redis-conf -n development
kubectl create configmap redis-conf --from-file=redis.conf -n development
