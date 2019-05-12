#### 一、创建mysql账户和数据目录
```shell
# 创建用户
groupadd mysql
useradd -r -g mysql -s /bin/false mysql
# 创建数据目录
mkdir -p /data/mysql3306/{mysql,binlog,slowlog,tmp,log,run}
mkdir -p /usr/local/mysql
chown -R mysql. /data/mysql3307
chown -R mysql. /usr/local/mysql
```
#### 二、mysql二进制下载
```shell
dir=`pwd` 
cd $dir
yum install -y wget && wget https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz
tar zxf mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz -C /usr/local/src
cp -r /usr/local/src/mysql-5.7.26-linux-glibc2.12-x86_64/* /usr/local/mysql
```
#### 三、初始化mysql
```shell
# 配置环境变量
echo "export PATH=$PATH:/usr/local/mysql/bin" >> /etc/profile
source /etc/profile
# 初始化
mysqld --defaults-file=/data/mysql3306/config/my.cnf --initialize --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql3306/mysql
# 配置ssl
mysql_ssl_rsa_setup --basedir=/usr/local/mysql --datadir=/data/mysql3306/mysql
# 手动启动
mysqld_safe --defaults-file=/data/mysql3307/config/my.cnf &
```
#### 四、mysql自启动
```shell
cp mysqld.service /usr/lib/systemd/system/mysqld.service
systemctl enable mysqld
systemctl start mysqld
```
##### 五、登录修改密码
```sql
more error.log | grep password
mysql -uroot -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Paswword1!';
flush privileges
```
##### 六、mysql多实例
```shell
# 初始化
mysqld --defaults-file=/data/mysql3306/config/my.cnf --initialize --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql3306/mysql
mysql_ssl_rsa_setup --basedir=/usr/local/mysql --datadir=/data/mysql3306/mysql
mysqld --defaults-file=/data/mysql3307/config/my.cnf --initialize --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql3307/mysql
mysql_ssl_rsa_setup --basedir=/usr/local/mysql --datadir=/data/mysql3307/mysql
# 启动
cp mysqld.service /usr/lib/systemd/system/mysqld3306.service
cp mysqld.service /usr/lib/systemd/system/mysqld3307.service
# 修改mysqld.service启动文件
Type=forking 改为 Type=sample
ExecStart启动命令改为/usr/local/bin/mysqld --defaults-file=/data/msyql3306/config/my.cnf
# 启动mysql
systemctl enable mysqld3306
systemctl start mysqld3306
```


