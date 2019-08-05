### mongo角色管理
#### mongo账户创建
```shell
# 验证权限
db.auth("root","passwd")
db.auth("root","123456")
db.auth("test","123456")
# 创建用户管理员
use admin
db.createUser(
	{
        user:"root",
        pwd:"123456",
        roles:[{role:"userAdminAnyDatabase",db:"admin"},"readWriteAnyDatabase"]
	}
)
# 创建普通用户
use test
db.createUser(
  {
    user: "test",
    pwd: "123456",
    roles: [ { role: "userAdminAnyDatabase", db: "test" } ]
  }
)
# 连接过程创建验证
mongo --port 27017 -u "myTester" -p "xyz123" --authenticationDatabase "test"
```

