#### 解决无法umount的问题
```shell
# 卸载
umount /Medical
umount: /Medical：目标忙
# 查看占用情况
fuser -mv  /Medical
/Medical:
root     kernel mount /Medical
root       5979 F.... c bash
# kill 调进程
kill -9 5979
# 在查看挂载情况
fuser -mv  /Medical
/Medical:
root     kernel mount /Medical
# 卸载
umount /Medical
```
