### 普罗米修斯监控搭建
#### pushgateway安装
```python
# 下载pushgateway
wget -c https://github.com/prometheus/pushgateway/releases/download/v0.8.0/pushgateway-0.8.0.linux-amd64.tar.gz
# 安装 pushgateway

```
#### prometheus安装
```python
# 下载prometheus
wget -c https://github.com/prometheus/prometheus/releases/download/v2.10.0/prometheus-2.10.0.linux-amd64.tar.gz

```
#### grafana安装
```python
# 添加yum存储库
cat >> /etc/yum.repos.d/grafa.repo << EOF
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF
# 安装grafana
yum install -y grafana
# 启动grafana
systemctl enable grafana-server
systemctl start grafana-server
```