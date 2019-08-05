### redis 常用命令
#### exists and del
```shell
setmykey a
OK
exists mykey
（integer）1
del mykey
（integer）1
exits mykey
（integer）0
exists 判断key是否存在，存在返回为1，不存在返回为0，del删除key
```
#### type and keys
```shell
set mykey a
OK
type mykey
string
keys my* 
1)"myset"
2)"mykey"
type  返回key的类型
keys my* 返回匹配的key列表
```
####  randomkey and clear
randomkey 随机获得一个已经存在的key

clear清除界面
#### rename and renamenx
rename oldname newname 改key的名字，新建如果存在将会被替换

renamenx oldname newname 改key的名字，新建如果存在将会失败

dbsize 返回当前数据库key的总数
####  限制key的生存时间
```shell
setmykey a
expire mykey10
getkey
"a"
getkey
（nil）
expire 设置key 的过期时间
ttl key  查询key的过期时间
flushdb  清除当前数据库中所有的键
flushall 清除所有数据库中的所有键
```
#### redis密码设置命令
```shell
config get requirepass （查看密码）
config set requirepass 123
auth 123
config get *max-*-xxx*  查询数据最大数量
config resetstat  重置数据统计
```
#### info 查看信息
1、server：redis server常规信息

2、clients：client 连接信息

3、memory：内存信息

4、persistence：rdb and aof 相关信息

5、stats：常规信息

6、replication：Master/slave 请求信息

7、cpu：cpu占用信息

8、cluster：redis集群信息

9、keyspace：数据库信息统计

10、all：返回所有信息

11、默认设置信息
