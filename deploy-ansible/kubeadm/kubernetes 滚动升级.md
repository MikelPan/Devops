<<<<<<< HEAD
#### deployment 滚动升级
```shell
# 查看应用部署状态
kubectl rollout status deployment/member-platform-console-test --namespace=dadi-saas-member-pre
# 滚动升级应用
kubectl set image deployment/member-platform-console-test member-platform-console-test=registry.cn-shenzhen.aliyuncs.com/dadi01/dadi-saas-member-web-front:1.1 --namespace=dadi-saas-member-pre --record
# 查看详情
kubectl describe deployment/member-platform-console-test --namespace=dadi-saas-member-pre
# 查看历史版本
kubectl rollout history deployment/member-platform-console-test --namespace=dadi-saas-member-pre
# 版本回滚
kubectl rollout undo deployment/member-platform-console-test --namespace=dadi-saas-member-pre --to-revision=1
# 暂停升级
kubectl rollout pause deployment/member-platform-console-test --namespace=dadi-saas-member-pre
# 继续升级
kubectl rollout resume deployment/member-platform-console-test --namespace=dadi-saas-member-pre
```
#### rc 滚动升级
```shell
# 升级
kubectl rolling-update rc-nginx-2 -f rc-nginx.yaml 
# 回滚
kubectl rolling-update rc-nginx-2 —rollback
# 伸缩
kubectl scale rc rc-nginx-3 —replicas=4
# 自动伸缩
kubectl autoscale rc rc-nginx-3 —replicas=4
```
=======
#### deployment 滚动升级
```shell
# 查看应用部署状态
kubectl rollout status deployment/console-test --namespace=pre
# 滚动升级应用
kubectl set image deployment/console-test console-test=registry.cn --namespace=pre --record
# 查看详情
kubectl describe deployment/console-test --namespace=pre
# 查看历史版本
kubectl rollout history deployment/member-platform-console-test --namespace=pre
# 版本回滚
kubectl rollout undo deployment/console-test --namespace=pre --to-revision=1
# 暂停升级
kubectl rollout pause deployment/console-test --namespace=pre
# 继续升级
kubectl rollout resume deployment/console-test --namespace=pre
```
#### rc 滚动升级
```shell
# 升级
kubectl rolling-update rc-nginx-2 -f rc-nginx.yaml 
# 回滚
kubectl rolling-update rc-nginx-2 —rollback
# 伸缩
kubectl scale rc rc-nginx-3 —replicas=4
# 自动伸缩
kubectl autoscale rc rc-nginx-3 —replicas=4
```
>>>>>>> 195cafcb9d90cfc16b986ef25929ede2bdb8d491
