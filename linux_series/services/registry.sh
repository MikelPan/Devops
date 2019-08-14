#### 一、harbor安装
```shell
# 安装docker-compose
curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
# 下载harbor
wget -c https://storage.googleapis.com/harbor-releases/release-1.8.0/harbor-offline-installer-v1.8.0-rc2.tgz
tar zxvf harbor-offline-installer-v1.8.0-rc2.tgz -C /usr/local
# 修改配置文件
vim harbor.yml
hostname: harbor.plyx.site
# 启动harbor
./install.sh
# 配置docker
vim /etc/docker/daemon.json
{   "data-root": "/data/docker",
    "registry-mirrors": ["http://9b2cd203.m.daocloud.io"],
    "insecure-registries": ["192.168.174.200:8100","harbor.plyx.site:8100"],
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "5"
    }
}
# 推动镜像
docker tag demo harbor.plyx.site:8100/spring_boot/demo
docker login harbor.plyx.site:8100
docker push harbor.plyx.site:8100/spring_boot/demo
```
#### 二、docker-registry安装
```shell
# 创建searcts
mkdir auth
docker run \
  --entrypoint htpasswd \
  registry:2 -Bbn mikel Password > auth/htpasswd
# 创建自签证书
mkdir certs
openssl req \
  -newkey rsa:4096 -nodes -sha256 -keyout certs/plyx.site.key \
  -x509 -days 365 -out certs/plyx.site.crt
# docker 私有仓库启动
docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name registry \
  -v "$(pwd)"/auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  -v "$(pwd)"/certs:/certs \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/plyx.site.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/plyx.site.key \
  registry:2
# 在需要推送镜像的主机中
拷贝证书到dockcer配置文件中 /etc/docker/certs.d/plyx.site/plyx.site.crt
systemctl restart docker
# 通过http方式安装
# 创建config.yml 文件
version: 0.1
log:
  fields:
    service: registry
storage:
  delete:
    enabled: true
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
    maxthreads: 100
  maintenance:
    uploadpurging:
      enabled: true
      age: 168h
      interval: 24h
      dryrun: false
    readonly:
      enabled: false
auth:
  htpasswd:
    realm: basic-realm
    path: /auth/htpasswd
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
    storagedriver:
        enabled: true
        interval: 10s
        threshold: 3
# 启动docker
docker run -d \
  --privileged \
  --restart=always \
  -p 5000:5000 \
  --name registry \
  -v $basepath/config.yml:/etc/docker/registry/config.yml \
  -v `pwd`/htpasswd:/auth/htpasswd \
  -v /home/registry/:/var/lib/registry/ \
  registry:2
```