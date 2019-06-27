### 一、加密查询
```shell
# md5加密
select MD5('123456') as a
# 掩藏身份证号
select CONCAT(LEFT(`id_number`,9),'*********',RIGHT(`id_number`,1))
# 查询身份证号
select * from test where left('id_number',6)=123456 and right('id_number',3)=456
# 生成随机数
select round(rand()*(999999-111111)+111111)
# 生成id流水号
set id = CONCAT(LEFT(id_number,6),'181206',LPAD(id, 7,'0'))  #从左到右截取
set id = CONCAT(LEFT(id_number,6),'181206',RPAD(id, 7,'0'))  #从右到左截取
# 添加性别
IF (MOD(SUBSTRING(id_number,17,1),2),'男','女') as "user_sex"
# 正则匹配
select * from table where clounme REGEXP '[A-Z]'
# 识别大小写
select * from test where id_number like 'x%'
```
### 二、去重查询
```shell
# 去重查询
select username from auth_user GROUP BY username HAVING COUNT(*) >4
select * from user where username in(select username from auth_user GROUP BY username HAVING COUNT(*) >1
# 去重删除
select id from user  where id_number in(select id_number from user group BY id_number HAVING COUNT(id_number) >1) and id not in (select min(id) from use_exit group by id_number having count(id_number)>1)
# 字段去重查询
select distinct census_county from user
# 字符串截取
select left('abcd',3)
select right('abcd',3)
select substring('abcd',2,2)
select substring('abcd',-2,2)
select substring('abcd',-2)
# 字符串转换日期格式
select FROM_UNXITIME(date_bitrh,'%Y%m%d') from a
```
### 三、连接查询
```shell
# 内连接查询
select * from table1 inner join table2 on table1.user=table2.user
# 左连接查询
select * from table1 left join table2 on table1.user=table2.user
# 右连接查询
select * from table1 right join table2 on table1.user=table2.user
# update 更新
update user a inner join user_regiter b on 
a.id_number=b.id_number set b.id=a.id,a.user_sex=b.user_sex,a.user_name=b.user_name
# 子查询更新
update user a,(select IF (MOD(SUBSTRING(id_number,17,1),2),'男','女')  as user_sex from user_1) b set a.user_sex=b.user_sex where a.id_number is not null
update user a,(select date_birth,id_number_enc from user_register_1) b set a.date_birth=b.date_birth where a.id_number=b.id_number
```
### 四、增加字段
```shell
# 增加字段
alter table user add is tinyint(1) comment '是否人员';
# 修改字段名
ALTER TABLE testalter_tbl CHANGE i j BIGINT;
ALTER TABLE testalter_tbl MODIFY c CHAR(10);
# 修改表名
ALTER TABLE testalter_tbl RENAME TO alter_tbl;
# 创建索引
CREATE INDEX indexName ON mytable(username(length));
# 添加普通索引
ALTER table tableName ADD INDEX indexName(columnName)
# 删除索引
DROP INDEX [indexName] ON mytable;
# 删除字段
ALTER table tableName drop cloumes
# 查看索引
show index from table;
# 创建唯一索引
CREATE UNIQUE INDEX indexName ON mytable(username(length))
# 添加索引
ALTER TABLE tbl_name ADD PRIMARY KEY (column_list)
ALTER TABLE tbl_name ADD UNIQUE index_name (column_list)
ALTER TABLE tbl_name ADD INDEX index_name (column_list)  # 普通索引，索引值可以出现多次
ALTER TABLE tbl_name ADD FULLTEXT index_name (column_list)
# 删除主键
ALTER TABLE testalter_tbl DROP PRIMARY KEY
# 增加字段类型长度
alter table 表名 modify column 字段名 char(19)
```
### 锁表
```shell
# 加读锁
SET AUTOCOMMIT=0;
lock tables user_auth_image read
COMMIT;
UNLOCK TABLES;
```