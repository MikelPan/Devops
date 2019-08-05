#### 设置密码
- 方法一
```shell
grep -n requirepass /etc/redis/redis.conf
sed -i 's@# requirepass@requirepass test@g' /etc/redis/redis.conf
service redis-server restart
redis-cli
auth peony_redis
redis-cli -a test
```
- 方法二
```shell
config set requiress test
```
#### 主从复制
1、master可以拥有多个slave

2、多个slave可以连接在同一个master上，还可以连接其他的slave，当master宕机后，相连的slave转变为master

3、主从复制不会阻塞master，再同步数据时，master 可以继续处理client请求

4、slave与master建立连接，发送sync同步命令

5、master会启动一个后台进程，将数据快照保存到文件中，同时master主进程会开始收集新的写命令并缓存

6、后台完成保存后，就将此文件发送给slave

7、slave将此文件保存在磁盘上
```shell
# 配置主从
vim /usr/local/redis/redis.conf  (主)
port 6379
bind 172.16.5.1 127.0.0.1
daemonize yes
pidfile        /var/run/redis_6379.pid
requirepass    redis
vim /usr/local/redis/redis.conf  (从)
port 6380
bind 172.16.5.2 127.0.0.1
daemonize yes
pidfile        /var/run/redis_6380.pid
masterauth     redis
# 登录客户端（主）
redis-cli -a redis
127.0.0.1:6379>set name redis-master
127.0.0.1:6379> info repliaction
# 登录客户端（从）
redis-cli -a redis
# 配置主从
127.0.0.1:6380> slaveof 127.0.0.1 6379
127.0.0.1:6380> info repliaction
127.0.0.1:6380>get name
```
#### 事务
只能client发起事务的命令可以连续执行，不会插入其他client命令，通过multi命令开始事务，后续的命令不会执行，被存放到一个对列中，当执行exec命令，redis顺序执行对列中所有命令，如果执行出错不会回滚。
```shell
multi
set name a
set name b
exec
get name
```
#### 持久化
1、快照，将数据放到文件中，默认方式

将内存中的数据已快照的方式写入二进制文件中，默认文件为dunp.rdb,可以通过配置设置自动作快照持久化的方式，可配置redis在n秒内如果超过m个key被修改就自动保存快照。

save 9001900秒内如果超过超过1个key被修改，则发起快照保存

save 30010300秒内如果超过10个key被修改，则快照保存

2、append-only file 将读写操作保存在文件中

由于快照方式在一定时间间隔作一次，所以如果redis意外down掉的话，就会丢失最后一次次快照后的所有修改

aof 比快照有更好的持久化，使用aof，redis将每一个收到的写命令都通过wirte函数写入到文件中当redis启动会通过重新执行文件中保存的写命令来在内存中重新建立整个数据的内容

使用fsync函数强制os写入到磁盘的时间

appendonly yes               // 启用aof持久化

\#appendfsync always    //  收到命令就写入磁盘，最慢，数据最完整

appendfsync everysec   // 每秒写入磁盘一次，性能和持久化方面做了折中

\#appendfsync no          // 完全依赖os，性能最好，持久化没有保证

