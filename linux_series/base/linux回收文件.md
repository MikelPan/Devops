### 一、创建回收脚本
```shell
# 创建回收文件夹
mkdir -p /home/.trash_tmp
# 创建回收脚本
cat > /usr/bin/trash <<EOF
#!/bin/bash
mv $@ /home/.trash_tmp
EOF
# 添加权限
chmod 755 /usr/bin/trash
chmod 777 /home/.trash_tmp
```
### 二、添加别名
```shell
cat >> /etc/bashrc << EOF
alias rm='/usr/bin/trash'
EOF
source /etc/bashrc
```
### 三、定时任务
```shell
* * */15 * * cd /home/.trash_tmp && find -name * -mtime +7 | xargs /usr/bin/rm
```
