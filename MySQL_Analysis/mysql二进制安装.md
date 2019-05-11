#### 一、创建mysql账户和数据目录
```python
# 创建用户
groupadd mysql
useradd -r -g mysql -s /bin/false mysql
# 创建数据目录
mkdir -p /data/mysql3306/{mysql,binlog,slowlog,tmp,log,run}
mkdir -p /usr/local/mysql
chown -R mysql. /data/mysql3306
chown -R mysql. /usr/local/mysql
```
#### 二、mysql二进制下载
```python
dir=`pwd` 
cd $dir
yum install -y wget && wget https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz
tar zxf mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz -C /usr/local/src
cp -r /usr/local/src/mysql-5.7.26-linux-glibc2.12-x86_64/* /usr/local/mysql
```
#### 三、初始化mysql
```python
# 配置环境变量
echo "export PATH=$PATH:/usr/local/mysql/bin" >> /etc/profile
source /etc/profile
# 初始化
mysqld --defaults-file=/etc/my.cnf --initialize --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql3306/mysql
# 配置ssl
mysql_ssl_rsa_setup --basedir=/usr/local/mysql --datadir=/data/mysql3306/mysql
# 手动启动
mysqld_safe --defaults-file=/etc/my.cnf &
```
#### 四、mysql自启动
```python
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


