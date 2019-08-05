#### 生成traefix-cert证书
##### 采用自签证书生成
```shell
# 安装cfssl
wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
chmod +x cfssl_linux-amd64
mv cfssl_linux-amd64 /usr/local/bin/cfssl

wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
chmod +x cfssljson_linux-amd64
mv cfssljson_linux-amd64 /usr/local/bin/cfssljson

wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
chmod +x cfssl-certinfo_linux-amd64
mv cfssl-certinfo_linux-amd64 /usr/local/bin/cfssl-certinfo

export PATH=/usr/local/bin:$PATH
# 签发根证书
cfssl gencert -initca ca-csr.json | cfssljson -bare ca
# 签发traefix tls证书
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes traefix-csr.json | cfssljson -bare traefix
```
##### 创建secret
新建/ssl目录,并将生成的证书改名称为tls.crt和tls.key
```shell
cp traefik.pem /ssl/tls.crt 
cp traefik-key.pem /ssl/tls.key
kubectl delete secret traefix-cert -n kube-system
kubectl create secret tls traefix-cert --cert=tls.crt --key=tls.key -n kube-system
```
##### 创建traefix-configmap
在tarefik 启动脚本目录下，创建traefik.toml文件并创建configmap traefik-conf
```shell
kubectl delete configmap traefik-conf -n kube-system
kubectl create configmap traefix-conf --from-file=traefik.toml -n kube-system
```
