### iptables 规则
#### 原地址,目的地址nat
适用于无外网ip的服务器需要访问互联网的场景下

serverA: 172.16.5.10 222.222.222.2

serverB: 172.16.5.11

*原地址转换*
```shell
# 指定服务器B的默认网关
echo "GATEWAY=172.16.5.10" >> /etc/sysconfig/entwork-scripts/if-enth0
# A上配置路由转发
sysctl -w net.ipv4.ip_forward=1
# A上配置iptables 规则
iptables -t filter -A FORWARD -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to 222.222.222.2
```
*目的地址转换*
```shell
# A上设置iptables规则
iptables -t nat -A PREROUTING -d 222.222.222.2 -p tcp -m tcp --dport 1521 -j DANT --to-destination 172.16.5.11:1521
iptables -t nat -A POSTROUTING -d 172.16.5.11 -p tcp -m tcp --dport 1521 -j SNAT --to-source 172.16.5.10
```