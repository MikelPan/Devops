### mongo使用
#### 集合
```shell
# 连接数据库
use mydb
# 印证密码
db.auth("root","passwd")
# 创建集合
db.createCollection("myset")
# 查看集合
show collections
# 删除集合
db.myset.drop()
# 集合中插入数据
db.myset.insert({title:'mongodb',by:'菜鸟教程',likes:100})
# 查看集群的数据
db.myset.find()
# 定义文档
document=({title:'mongodb',by:'菜鸟教程'})
# 插入文档
db.myset.insert(document)
# 集合数据清空
db.myset.remove({})
# mongodb 条件操作符
(>) 大于 - $gt
(<) 小于 - $lt
(>=) 大于等于 - $gte
(<=) 小于等于 - $lte
# 查询大于100的数据
db.myset.find({likes:{$gt:100}})
# 查询大于等于100数据
db.myset.find({likes:{$gte:100}})
# 查询小于等于100的数据
db.myset.find({likes:{$lte:150}})
# 查询小100的数据
db.myset.find({likes:{$lt:150}})
# 查询大于100小于200的数据
db.myset.find({likes:{$lt:100,$gt:200})
# mongodb limit方法
db.myset.find().limit(5)
# mongodb skip方法
db.myset.find().limit(5).skip(1)
# sort排序方法
db.myset.find().sort({"title":1}) # 正序
db.myset.find().sort({"title":-1) # 倒序
```
#### 索引
```shell
# 创建索引
db.myset.createIndex({"title":1})
db.myset.createIndex({"title":1,"age":-1})
# 后台创建索引
db.myset.createIndex({"title":1,"age":-1},{backgroud:true})
# 查看索引
db.myset.getIndexes()
# 查看索引大小
db.myset.totalIndexSize()
# 删除集合所有的索引
db.myset.dropIndexes()
# 删除集合指定索引
db.myset.dropIndex("myset")
```
#### 聚和
```shell
# 聚合aggregate
db.COLLECTION_NAME.aggregate({
    $match:{x:1},
    {limit:NUM},
    $group:{_id:$age}
})
$match ： 查询更find一样
$limit :  限制显示结果数量
$skip  :  忽略结果数量
$sort  :  排序
$group :  按照给定表达式组合结果
emplax:
db.myset.aggregate([{$group:{_id:"$name",user:{$sum:"$user_id"}}}])
# 聚合表达式
$sum 计算总和
$avg 计算平均值
$min和$max 计算最大值和最小值
$push      在结果文档中插入值到一个数组
$addToset  在结果文档中插入一个数组，但是不创建副本
$first     根据资源文档的排序获取第一个文档数据
$last      根据资源文档的排序获取最后一个文档数据
```