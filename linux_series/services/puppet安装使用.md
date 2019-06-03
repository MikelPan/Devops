### Puppet 下载安装
```python
# 下载puppet源码包
wget -c https://codeload.github.com/puppetlabs/puppet/tar.gz/6.4.2
# 安装pupper server
hostnamectl hostname puppet # 设置主机名
rpm -Uvh https://yum.puppet.com/puppet6-release-el-7.noarch.rpm
yum install -y puppetserver
# 安装puppet agent
rpm -Uvh https://yum.puppet.com/puppet6-release-el-7.noarch.rpm
yum install -y puppet-agent
# 添加host解析
cat >> /etc/hosts <<EOF
192.168.174.10 puppet.master.com
192.168.174.11 puppet.client.com
EOF
# 修改jvm 启动参数
cat >> /etc/sysconfig/puppetserver <<EOF
JAVA_ARGS="-Xms512m -Xmx512m
EOF
# 添加环境变量
echo "PATH=/opt/puppetlabs/server/apps/puppetserver/bin/:$PATH" >> /etc/profile
# 修改配置
cat >> /etc/puppetlabs/puppet/puppet.conf <<EOF
certname = puppet.master.com
systemctl enble puppetserver
puppetserver ca setup
systemctl start puppetserver
# 编辑client配置文件
echo "PATH=/opt/puppetlabs/puppet/bin:$PATH" >>/etc/profile # 客户端配置环境变量
cat >> /etc/puppetlabs/puppet/puppet.conf <<EOF
[main]
server = puppet.master.com
certname = puppet.client.com
EOF
systemctl enable puppet
systemctl start puppet
# msater签署签名请求
puppetserver ca list --all
puppetserver ca sign --certname puppet.client.com
```

