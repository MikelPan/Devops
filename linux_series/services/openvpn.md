### 阿里云上使用openvpn
#### 更新阿里云镜像源
```shell
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
wget -qO /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
yum clean metadata
yum makecache
```
#### 安装依赖包
```shell
yum install -y lzo lzo-devel openssl openssl-devel pam pam-devel
yum install -y pkcs11-helper pkcs11-helper-devel
```
#### 安装openvpn服务
```shell
# 下载openvpn 源码包
wget http://oss.aliyuncs.com/aliyunecs/openvpn-2.2.2.tar.gz
yum install -y rpm-build
# rpmbuild 打包为rpm包
rpmbuild -tb openvpn-2.2.2.tar.gz
# 安装openvpn rpm包
rpm -ivh openvpn-2.2.2-1.x86_64.rpm
```
#### 配置openvpn服务端
```shell
# 修改vars配置文件
vim /root/rpmbuild/BUILD/openvpn-2.2.2/easy-rsa/2.0/vars
export KEY_COUNTRY="CN"   所在的国家
export KEY_PROVINCE="GuangDong"  所在的省份
export KEY_CITY="ShenZhen"   所在的城市
export KEY_ORG="IT"        所属的组织 
export KEY_EMAIL=plyx_46204@126.c0m   邮件地址
# 生成证书
ln -s openssl-1.0.0.cnf openssl.cnf
source ./vars
./clean-all
# 创建ca证书
./build-ca
替换Unit-name    为部门名
替换common name  为服务器的全域名
# 生成服务器证书
./build-key-server openvpnserver
# 生成秘钥和证书
./build-key openvenclient
# 生成客户端验证Diffie Hellman
./build-dh
# 增加安全性
openvpn --genkey --secret keys/ta.key
# 复制证书、密钥和参数文件
cp /root/rpmbuild/BUILD/openvpn-2.2.2/easy-rsa/2.0/keys/* /etc/openvpn/
cp /root/rpmbuild/BUILD/openvpn-2.2.2/sample-config-files/server.conf /etc/openvpn/
# 修改server 配置
vim server.conf
local 0.0.0.0  请在此处填写您的云服务器的公网IP地址
port 1194
proto udp
dev tun
ca ca.crt
cert aliyuntest.crt   请在此处填写生成服务器端证书时您自定义的crt名称
key aliyuntest.key   请在此处填写生成服务器端证书时您自定义的key名称
tls-auth /etc/openvpn/ta.key 0
dh dh1024.pem
server 172.16.0.0 255.255.255.0   # 不要和其他网段重复和冲突
push "route 172.18.81.0 255.255.255.0"
ifconfig-pool-persist ipp.txt
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 223.5.5.5"
client-to-client
keepalive 10 120
comp-lzo
user nobody
group nobody
persist-key
persist-tun
status /var/log/openvpn/openvpn-status.log
log    /var/log/openvpn/openvpn.log
verb 4
# 配置防火墙规则
yum install -y iptables-services
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.cnf
sysctl -p
iptables -t nat -A POSTROUTING -s 172.16.0.0/24 -o eth0 -j MASQUERADE
iptables -A INPUT -p tcp -m tcp --dport 1194 -j ACCEPT
iptables -A FORWARD -i tun+ -j ACCEPT
iptables -A FORWARD -i eth+ -j ACCEPT
# 加入nat转发
iptables -t nat -A POSTROUTING -o eth0  -j MASQUERADE
iptables -t nat -A POSTROUTING -o eth0  -j MASQUERADE
service iptables save
# 在目标服务器上添加路由
route add -net 172.16.0.0/24 gw 172.18.81.xx
# 启动openvpn
/usr/sbin/openvpn --config /etc/openvpn/server.conf &
```
#### 安装openvpn客户端
```shell
# linux 环境下安装openvpn
yum install -y openvpn
vim /etc/openvpn/conf/client.conf
client
dev tun
proto tcp
remote 203.195.xxx.xxx 1194  # OpenVPN服务器的外网IP和端口
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
ns-cert-type server 
tls-auth ta.key 1  # 客户端是1，服务器是0
comp-lzo
verb 3
# 启动openvpn
openvpn --daemon --config /etc/openvpn/conf/client.conf > /var/log/openvpn_client.log
```

