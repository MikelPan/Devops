#### linux 别名的使用
linux 重命名命令 alias ，它的作用为如果要执行命令太长又不符合用户的习惯，那么我们可以为它指定一个别名。alias 是命令的一种别称，输入alias查看已设置别名的命令。
##### 设置别名
全局配置在/etc/profile文件中，单用户配置在~/.bashrc文件中配置

*配置kubernetes 别名*
```shell
# 操作资源的别名
alias kcd='kubectl describe po'
alias kca='kubectl apply -f'
alias kcdp='kubectl delete po'
alias kcl='kubectl logs -f'
alias kcn='kubectl get nodes -o wide'
alias kcp='kubectl get po -o wide -A'
alias kce='kubectl get endpoints -A'
alias kcs='kubectl get svc -o wide -A'
alias kc='kubectl'
```

