#### 一、安装java环境
```shell
# 下载jdk软件包
wget https://download.oracle.com/otn/java/jdk/8u212-b10/59066701cf1a433da9770636fbc4c9aa/jdk-8u212-linux-x64.tar.gz
tar zxvf jdk-8u212-linux-x64.tar.gz -C /usr/local/src
mv /usr/local/src/jdk-8u212 /usr/local/jdk-8u212
# 配置java环境变量
cat >> /etc/prifile <<EOF
JAVA_HOME=/usr/local/jdk1.8.0_212/
JRE_HOME=$JAVA_HOME/jre
CLASS_PATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
export JAVA_HOME JRE_HOME CLASS_PATH PATH
EOF
source /etc/profile
```
#### 二、安装elastic
```shell
# 下载elastic
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.0.1-linux-x86_64.tar.gz
tar zxvf elasticsearch-7.0.1-linux-x86_64.tar.gz -C /usr/local/src
mv /usr/local/src/elasticsearch-7.0.1 /usr/lcoal/elasticsearch-7.0.1
# 创建账户，目录
groupadd elastic
useradd -r -g rlastic -s /bin/false elastic
chmod -R elastic. /usr/lcoal/elasticsearch-7.0.1
mkdir /var/lib/elasticsearch
mkdir /var/log/elasticsearch
chmod -R elastic. /var/lib/elasticsearch
chmod -R elastic. /var/log/elasticsearch
# 配置环境变量
cat >> /etc/profile <<EOF
echo "PATH=$PATH:/usr/local/elasticsearch-7.0.1/bin" >> /etc/profile
EOF
source /etc/profile
# 修改配置文件
vim /usr/local/elasticsearch-7.0.1/config/elasticsearch.yml
------------------------------------start----------------------------------------------
network.host: 0.0.0.0
http.port: 9200
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
-------------------------------------end-----------------------------------------------
# 启动elastic
elasticsearch -d
```
#### 三、安装kibana
```shell
# 下载kinaba
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.0.1-linux-x86_64.tar.gz
tar zxvf kibana-7.0.1 -C /usr/local/src
mv /usr/local/src/kibana-7.0.1 /usr/local/kibana-7.0.1
# 修改配置文件
vim /usr/local/src/kibana-7.0.1/config/kibana.yml
-------------------------------------------start----------------------------------------
elasticsearch.url: "http://0.0.0.0:9200"
server.host: "0.0.0.0"
kibana.index: ".kibana"
-------------------------------------------end-------------------------------------------
# 启动kibana
/usr/local/src/kibana-7.0.1/bin/kibana &
```
#### 四、安装filebeat
```shell
# 下载filebeat
wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.0.1-linux-x86_64.tar.gz
tar zxvf filebeat-7.0.1-linux-x86_64.tar.gz -C /usr/local/src
mv /usr/local/src/filebeat-7.0.1 /usr/local/filebeat-7.0.1
# 修改配置文件
vim /usr/local/filebeat-7.0.1/filebeat.yml
-----------------------------------start-----------------------------------------------
filebeat.prospectors:
- type: log
  enabled: true
  paths:
    - /var/xxx/*.log
    - /var/xxx/*.out
  multiline.pattern: ^\[
  multiline.negate: true
  multiline.match: after
  
  # json格式
  json.keys_under_root: true
  json.add_error_key: true
  json.message_key: log
  json.overwrite_keys: true
  
  # 标识字段
  fields:
    log_type: gateway
   
setup.kibana:
  host: "localhost:5601"
  
# 输出使用自定义索引名称
setup.template.name: "cobee"
setup.template.pattern: "cobee-*"

# 数据输出目标地址
output.elasticsearch:
  hosts: ["localhost:9200"]
  index: "xhg-ms-%{+yyyy.MM.dd}"
--------------------------------------end---------------------------------------------
# 启动filebeat
./usr/local/filebeat-7.0.1/filebeat -c /usr/local/filebeat-7.0.1/filebeat.yml
```





