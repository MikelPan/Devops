### 运维自动化-Ansible
#### Ansible安装
```shell
yum install -y ansible
```
**Ansible常规使用**
```shell
# 查看模块
ansible-doc -l 查询模块用法
ansible-doc -s nginx 查询指定模块用法
```
#### ansible-galaxy使用
```shell
连接 https://galaxy.ansible.com下载相应的roles，此网站是Ansible爱好者将日常使用较好的playbooks打包上传，其他人可以免费下载
到Ansible PlayBooks并立即投入使用。
# 直接按作者搜索
ansible-galaxy search --author geerlingguy
# 下载对应的roles
ansible-galaxy install -p /root/ansible-playbook geerlingguy.mysql
# 批量下载
编辑下载文件requirements.yml，在执行命令批量下载
vim requirements.yml
--------------------------------------------start-----------------------------------------
# Nginx 1.10
- src: williamyeh.nginx
 path:  path: /root/ansible-playbook

# PHP 7
- src: chusiang.php7
 path:  path: /root/ansible-playbook

# MySQL 5.6
- src: geerlingguy.mysql
 path: /root/ansible-playbook
---------------------------------------------end------------------------------------------
ansible-galaxy install -f -p /root/ansible-playbook -r requirements.yml
```


