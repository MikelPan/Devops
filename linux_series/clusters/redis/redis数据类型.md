### redis 数据类型
------
#### string 字符串
```shell
# redis 设置字符串
127.0.0.1:6379>setmykey abc
OK
127.0.0.1:6379>getmykey
"abc"
EX seconds − 设置指定的到期时间(以秒为单位)。
PX milliseconds-设置指定的到期时间(以毫秒为单位)。
NX-仅在键不存在时设置键。
XX-只有在键已存在时才设置
```
#### redis 加法计算
```shell
# 加法运算
set a 100 
incr a
（integer）101
incr a 
（integer）102 
incrby a 100
（integer) 202
incr 每次加1
incrby 加法运算
```
#### redis创建数组
```shell
# 创建数组
mset a 10 b 10 c 10
mget a b c
1) "10"
2）"10"
3）"10"
```
#### redis 列表
```shell
rpush mylist A
(integer) 1
rpush mylist B
(integer) 2
lpush mylist first
(integer) 3
lrange mylist 0-1
1)"first"
2)"A"
3)"B"
del mylist
rpush mylist a
rpush mylist b
lpush mylist c
lrange mylist 0-1
1)"c"
2)"a"
3)"b"
lpop mylist
"c"
lrange mylist 0-1
1)"a"
2)"b"
rpop mylist
"b"
lrange mylist 0-1
1)"a"
rpush 插入一个新的列表在尾部
lpush 插入一个新的列表在首部
lrange 检索0第一个-1最后一个
del 删除列表
lpop 从前将列表中元素剔除
rpop 从后将列表中元素剔除
redis 不存储空列表，当列表中元素被删除后，自动删除空列表
```
#### redis hashes
```shell
hmset user:a usernam sb birth10 verfile1
hget user:a username
"sb"
hget user:a birth
"10"
hgetall user:a
1)"username"
2)"sb"
3）"birth"
4)"10"
5)"verfile"
6)"1"
hmget user:a username birth c
1)"sb"
2)"10"
3) (nil)
hincrby user:a birth10
(integet) 20
redis hashes 字符串和字符字段之间的映射，展现对象的完美数据类型
hmset 设置多域的hash表
hgetall 获取指定key的所有信息
hget 获取单域的信息
hmget 获取多域的信息，返回为数组
hincrby hash字符加法运算
```
#### redis 集合
set为无序集合，不包含相同的元素，支持不通集合合并，交集，找出不同的元素
```shell
sadd myset a b c
(integer) 3
smembers myset
1)"a"
2)"b"
3)"c"
sismember myset1
(integer) 1
sismember myset0
(integer) 0
sismember myset a
(integer) 1
sismember mys3
(integer) 0
sadd 创建无序集合
smember 查看集合
sismember 匹配集合名称，内容及个数，成功返回为1，失败返回为0
```
有序集合，集合的成员唯一，前面有参数用来排序，访问速度快，提高性能
```shell
zadd hackers 1"a"2"b"3"c"
(integer)1
zrange hackers 0-1
1)"a"
2)"b"
3)"c"
zrevrange hackers 0-1
1)"c"
2)"b"
3)"a"
zrange hackers 0-1 withscores
1)"a"
2)"1"
3)"b"
4)"2"
5)"c"
6)"3"
zadd 创建有序集合，集合名称必须为两位以上包含两位，需要加上序号参数
zrange 正序查看集合
zrevrange 倒序查看集合
withscores  返回参数记录值
```

