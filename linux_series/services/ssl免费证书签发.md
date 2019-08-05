### 安装证书安装脚本
```shell
curl https://get.acme.sh | sh
alias acme.sh=~/.acme.sh/acme.sh
```
### 证书签发
```shell
# 使用http方式
acme.sh --issue -d esofar.cn -d www.esofar.cn -w /home/wwwroot/esofar.cn
# 使用dns 方式
acme.sh --issue -d *.clsn.io -d clsn.io --dns --yes-I-know-dns-manual-mode-enough-go-ahead-please # 添加A记录
dig -t txt  _acme-challenge.clsn.io @8.8.8.8 # 验证证书
acme.sh --renew  -d *.clsn.io -d clsn.io --dns --yes-I-know-dns-manual-mode-enough-go-ahead-please # 生成证书

# 使用dns api方式
api 参考文档 https://github.com/Neilpang/acme.sh/tree/master/dnsapi
export Ali_Key="ali-key"
export Ali_Secret="ali-secret"
acme.sh --issue --dns dns_ali -d plyx.site -d *.plyx.site
```

#### 说明参数的含义：

- --issue是 acme.sh 脚本用来颁发证书的指令；
- -d是--domain的简称，其后面须填写已备案的域名；
- -w 是--webroot的简称，其后面须填写网站的根目录

```shell
# 查看证书
acme.sh --list
# 删除证书
acme.sh remove plyx.site
```
### 安装证书
生成的证书放在了/root/.acme.sh/esofar.cn目录，因为这是 acme.sh 脚本的内部使用目录，而且目录结构可能会变化，所以我们不能让 Nginx 的配置文件直接读取该目录下的证书文件。
```shell
acme.sh  --installcert -d plyx.site \
         --key-file /etc/nginx/ssl/plyx.site.key \
         --fullchain-file /etc/nginx/ssl/fullchain.cer \
         --reloadcmd "service nginx force-reload"
```
### 合并证书
```shell
cat fullchain.cer plyx.site.key > haproxy.crt
```
### 更新证书
```shell
acme.sh --renew -d plyx.site --force
```
### 更新脚本
升级到最新版
```shell
acme.sh --upgrade
```
自动更新
```shell
# 开启自动更新
acme.sh  --upgrade  --auto-upgrade
# 关闭自动更新
acme.sh  --upgrade  --auto-upgrade 0
```
定时任务更新
```shell
22 0 * * * "/root/.acme.sh"/acme.sh --cron --home "/root/.acme.sh" > /dev/null
```