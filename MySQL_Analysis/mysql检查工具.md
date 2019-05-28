### 一、mysqldumpslow工具使用
#### 1.1、修改配置文件开启慢查询
**mysql 开启慢查询**
```shell
systemctl stop mysqld
echo -e "# 开启慢查询\nslow_query_log = 1\nslow_query_log_file = /var/lib/mysql/slow-query.log\nlong_query_time = 1\nlog_queries_not_using_indexes = 1" >>/etc/my.cnf
# 重启mysql
systemctl restart mysqld
# 登录mysql
mysql -uroot -pP@ssw0rd1
select sleep(1);
```
#### 1.2、修改变量开启慢查询
```sql
set global slow_query_log='ON';
set global slow_query_log_file='/var/lib/mysql/logs/slow.log';
set global long_query_time=1;
```
**使用mysqldumpslow 工具分析 慢查询日志**

- -s：排序方式，值如下
  
   c：查询次数
    
   t：查询时间
    
   l：锁定时间
    
   r：返回记录
    
   ac：平均查询次数
    
   al：平均锁定时间
    
   ar：平均返回记录书
    
   at：平均查询时间

- -t：top N查询

- -g：正则表达式

1、访问次数最多的5个sql语句
```shell
mysqldumpslow -s c -t 5 /var/lib/mysql/slow-query.log  
----------------------------------start----------------------------------------
Reading mysql slow query log from /var/lib/mysql/slow-query.log
Count: 2  Time=1.50s (3s)  Lock=0.00s (0s)  Rows=1.0 (2), root[root]@localhost
  select sleep(N)

Died at /usr/bin/mysqldumpslow line 161, <> chunk 2.
----------------------------------end-------------------------------------------
```
### 二、mysqlsla工具使用

**mysqlsla安装**
```shell
wget http://hackmysql.com/scripts/mysqlsla-2.03.tar.gz
tar zxvf mysqlsla-2.03.tar.gz -C /usr/local/src
cd /usr/local/src/mysqlsla-2.03
yum install -y perl-ExtUtils-CBuilder perl-ExtUtils-MakeMaker
yum install -y perl-DBD-MySQL
perl Makefile.PL
make && make install
```
**mysqlsla 分析慢查询日志**
```shell
mysqlsla -lt slow -sf "+select,update,insert" -top 10 slow.log > /root/test_time.log
mysqlsla -lt slow -sf "+select,update,insert" -top 10 -sort c_sum -db databasename slow.log > /root/test_time.log
```
**通过mysqlsla 查询日志分析**
```shell
mysqlsla -lt slow -sf "+select" -top 10 /var/lib/mysql/slow-query.log
---------------------------------start--------------------------------------
Report for slow logs: /var/lib/mysql/slow-query.log
2 queries total, 1 unique
Sorted by 't_sum'
Grand Totals: Time 3 s, Lock 0 s, Rows sent 2, Rows Examined 0


______________________________________________________________________ 001 ___
Count         : 2  (100.00%)
Time          : 3.001489 s total, 1.500745 s avg, 1.000509 s to 2.00098 s max  (100.00%)
Lock Time (s) : 0 total, 0 avg, 0 to 0 max  (0.00%)
Rows sent     : 1 avg, 1 to 1 max  (100.00%)
Rows examined : 0 avg, 0 to 0 max  (0.00%)
Database      : 
Users         : 
	root@localhost  : 100.00% (2) of query, 100.00% (2) of all users

Query abstract:
SELECT sleep(N);

Query sample:
select sleep(1);
---------------------------------end--------------------------------------
```
### 三、pt工具使用
**pt 工具安装**
```shell
#!/bin/bash
percona-toolkit-yum-install(){
# 下载最新版percona-toolkits 包
下载地址：https://www.percona.com/downloads/
wget -P /tar https://www.percona.com/downloads/percona-toolkit/3.0.12/binary/redhat/7/x86_64/percona-toolkit-3.0.12-re3a693a-el7-x86_64-bundle.tar
tar xvf /tar/percona-toolkit-3.0.12-re3a693a-el7-x86_64-bundle.tar 
# 安装依赖
yum install -y perl perl-DBI perl-DBD-MySQL perl-Time-HiRes perl-IO-Socket-SSL perl-Digest-MD5
rpm -ivh percona-toolkit-3.0.12-1.el7.x86_64.rpm
}
percona-toolkit-unline-install(){
# 安装离线安装包
rpm -ivh /percona-yum/*.rpm
rpm -ivh percona-toolkit-3.0.12-1.el7.x86_64.rpm 
}
--create-review-table  当使用--review参数把分析结果输出到表中时，如果没有表就自动创建
--create-history-table  当使用--history参数把分析结果输出到表中时，如果没有表就自动创建
--filter  对输入的慢查询按指定的字符串进行匹配过滤后再进行分析
--limit   限制输出结果百分比或数量，默认值是20,即将最慢的20条语句输出，如果是50%则按总响应时间占比从大到小排序，输出到总和达到50%位置截止。
--host  mysql服务器地址
--user  mysql用户名
--password  mysql用户密码
--history   将分析结果保存到表中，分析结果比较详细，下次再使用--history时，如果存在相同的语句，且查询所在的时间区间和历史表中的不同，则会记录到数据表中，可以通过查询同一CHECKSUM来比较某类型查询的历史变化。
--review 将分析结果保存到表中，这个分析只是对查询条件进行参数化，一个类型的查询一条记录，比较简单。当下次使用--review时，如果存在相同的语句分析，就不会记录到数据表中。
--output 分析结果输出类型，值可以是report(标准分析报告)、slowlog(Mysql slow log)、json、json-anon，一般使用report，以便于阅读。
--since 从什么时间开始分析，值为字符串，可以是指定的某个”yyyy-mm-dd [hh:mm:ss]”格式的时间点，也可以是简单的一个时间值：s(秒)、h(小时)、m(分钟)、d(天)，如12h就表示从12小时前开始统计。
--until 截止时间，配合—since可以分析一段时间内的慢查询
```
1、percona-toolkit用法
```shell
# 查看慢查询日志
pt-query-digest slow-query.log
--------------------------------------start---------------------------------------
# 280ms user time, 40ms system time, 25.93M rss, 220.21M vsz
# Current date: Wed Jan  2 14:51:50 2019
# Hostname: localhost.localdomain
# Files: slow-query.log
# Overall: 2 total, 1 unique, 0.00 QPS, 0.01x concurrency ________________
# Time range: 2018-12-29T08:56:22 to 2018-12-29T09:04:54
# Attribute          total     min     max     avg     95%  stddev  median
# ============     ======= ======= ======= ======= ======= ======= =======
# Exec time             3s      1s      2s      2s      2s   707ms      2s
# Lock time              0       0       0       0       0       0       0
# Rows sent              2       1       1       1       1       0       1
# Rows examine           0       0       0       0       0       0       0
# Query size            30      15      15      15      15       0      15

# Profile
# Rank Query ID                           Response time Calls R/Call V/M  
# ==== ================================== ============= ===== ====== =====
#    1 0x59A74D08D407B5EDF9A57DD5A41825CA 3.0015 100.0%     2 1.5007  0.33 SELECT

# Query 1: 0.00 QPS, 0.01x concurrency, ID 0x59A74D08D407B5EDF9A57DD5A41825CA at byte 565
# This item is included in the report because it matches --limit.
# Scores: V/M = 0.33
# Time range: 2018-12-29T08:56:22 to 2018-12-29T09:04:54
# Attribute    pct   total     min     max     avg     95%  stddev  median
# ============ === ======= ======= ======= ======= ======= ======= =======
# Count        100       2
# Exec time    100      3s      1s      2s      2s      2s   707ms      2s
# Lock time      0       0       0       0       0       0       0       0
# Rows sent    100       2       1       1       1       1       0       1
# Rows examine   0       0       0       0       0       0       0       0
# Query size   100      30      15      15      15      15       0      15
# String:
# Hosts        localhost
# Users        root
# Query_time distribution
#   1us
#  10us
# 100us
#   1ms
#  10ms
# 100ms
#    1s  ################################################################
#  10s+
# EXPLAIN /*!50100 PARTITIONS*/
select sleep(2)\G
-------------------------------------end-----------------------------------------
```
2、pt常规用法
```shell
pt-query-digest  slow.log > slow_report.log
pt-query-digest  --since=12h  slow.log > slow_report2.log
pt-query-digest slow.log --since '2014-04-17 09:30:00' --until '2014-04-17 10:00:00'> > slow_report3.log
pt-query-digest--filter '$event->{fingerprint} =~ m/^select/i' slow.log>slow_report4.log
pt-query-digest--filter '($event->{user} || "") =~ m/^root/i' slow.log> slow_report5.log
pt-query-digest--filter '(($event->{Full_scan} || "") eq "yes") ||(($event->{Full_join} || "") eq "yes")' slow.log> slow_report6.log
pt-query-digest  --user=root –password=abc123 --review  h=localhost,D=test,t=query_review --create-review-table  slow.log
pt-query-digest  --user=root –password=abc123 --review  h=localhost,D=test,t=query_ history--create-review-table  slow.log_20140401
pt-query-digest  --user=root –password=abc123--review  h=localhost,D=test,t=query_history--create-review-table  slow.log_20140402
# 通过tcpdump抓取mysql的tcp协议数据，然后再分析
tcpdump -s 65535 -x -nn -q -tttt -i any -c 1000 port 3306 > mysql.tcp.txt
pt-query-digest --type tcpdump mysql.tcp.txt> slow_report9.log
# 分析binlog
mysqlbinlog mysql-bin.000093 > mysql-bin000093.sql
pt-query-digest  --type=binlog  mysql-bin000093.sql > slow_report10.log
# 分析general log
pt-query-digest  --type=genlog  localhost.log > slow_report11.log
```